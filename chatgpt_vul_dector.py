#  Copyright [2022] [MA WEI @ NTU], ma_wei@ntu.edu.sg

#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0

#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#load parsers
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage
)
import os
import json
import glob
import time
from dotenv import load_dotenv
from global_logger import Log
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# chat mode instance

logger = Log.get_logger()

from utils.tool import remove_comments_and_docstrings, split_functions
import os
import tiktoken


def num_tokens_from_messages(value, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        num_tokens += len(encoding.encode(value))
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")

def parse_soldity_project(folder):
    project_code = []
    for sfile in glob.glob( f"{folder}/**/*.sol", recursive=True):
        fname = os.path.basename(sfile)
        srccode = open(sfile).read()
        srccode = remove_comments_and_docstrings(srccode)
        project_code.append({"code":srccode, "filename":fname})
    return project_code
    
def load_vul_examples(vul_folder= "datasets/solidity_vul/not-so-smart-contracts", query_method="oneshot"):
    vul_code = {}
    if query_method == "oneshot":
        for vul_type in os.listdir(vul_folder):
            vul_type_path = os.path.join( vul_folder, vul_type)
            details = open( os.path.join(vul_type_path, "README.md") , "r").read()
            examples = []
            for sfile in glob.glob( f"{vul_type_path}/**/*.sol", recursive=True):
                srccoide = open(sfile).read()
                srccoide = remove_comments_and_docstrings(srccoide)
                examples.append( srccoide )
            assert len(examples) != 0, f"No example for one shot {len(examples)}"
            src_code = " \n ".join(examples)
            vul_code[vul_type]=( {"code":src_code, "details":details} )
        return vul_code
    elif query_method == "concept":
        for vul_type in os.listdir(vul_folder):
            vul_type_path = os.path.join( vul_folder, vul_type)
            details = open(vul_type_path).read()
            v = vul_type.replace(".md", "")
            vul_code[v]=( {"details":details} )
        return vul_code
    else:
        assert False, f"Parameter Error query_method, {query_method}"

def create_prompt_one_shot(user_input, one_shot_exmaple):
    #print(one_shot_exmaple)
    system_prompt = """Please analyze the following smart contract code for potential vulnerabilities, considering the example code and vulnerability details provided. Identify any vulnerabilities in the new code and explain the reasons behind them. Your report should inlcude the vulnerable type and its details in the Markdown format. \n""" + \
    """Example Code:  
    ```Solidity 
        """+one_shot_exmaple['code'] +"""
    ```\n\n""" + \
    """Vulnerability Details of Example Code: \n """ + \
    """``` 
    """+ one_shot_exmaple['details'] + """\n```\n\n""" + \
    """Input New Smart Contract Code to Analyze: \n""" + \
    """ ```Solidity \n""" + \
    user_input + \
    """\n```"""
    #print('Done creating prompt')
    return [system_prompt]

def create_prompt_concept(user_input, concept):
    #print(one_shot_exmaple)
    system_prompt = """Please analyze the following smart contract code for potential vulnerabilities, considering the vulnerability concept and details provided. Identify any vulnerabilities in the new code and explain the reasons behind them. Your report should inlcude the vulnerable type and its details in the Markdown format. \n""" + \
    """Vulnerability Details of Example Code: \n """ + \
    """``` 
    """+ concept['details'] + """ 
    ```\n\n\n""" + \
    """Input New Smart Contract Code to Analyze: """ + \
    """ 
    ```Solidity 
    """ + user_input + """
    ```"""
    #print('Done creating prompt')
    return [system_prompt] 

def split_file(code):
    code_fn = split_functions(code)
    def split_list(input_list, chunk_size=5):
        return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]
    keys_chunk = split_list(list(code_fn.keys()))
    code_pieces = []
    for chunk in keys_chunk:
        fns = [ ]
        for k in chunk:
            fns.append( code_fn[k] )
        code_pieces.append("\n".join(fns))
    return code_pieces

import json
def chat_gpt_answer(data_eggs, vul_code, output_dir, query_method ):
    prompt_methods = {"oneshot":create_prompt_one_shot, "concept":create_prompt_concept}
    createrPrompt = prompt_methods[query_method]
    os.makedirs(os.path.join(f"{output_dir}"), exist_ok=True)
    for v in vul_code:
        for ex in data_eggs:
            code = ex["code"]
            filename = ex["filename"]
            filename = filename.replace(".sol", "")
            os.makedirs(os.path.join(f"{output_dir}/{filename}"), exist_ok=True)
            outputfile_answer = os.path.join(f"{output_dir}/{filename}/{v}_answer.md")
            questions_list = [ createrPrompt(code, vul_code[v]) ]
            one_question = "".join(questions_list[0])
            if num_tokens_from_messages( one_question ) > 4097:
                code = remove_comments_and_docstrings(code)
                code_pieces = split_file(code) # (a, b, c) (dfdf)
                questions_list = [ createrPrompt(c, vul_code[v]) for c in code_pieces ] # op 
                for q in questions_list:
                    print(num_tokens_from_messages( q ) )
            answers = [ ]
            qlist = []
            for question in questions_list:
                messages = [
                    SystemMessage(content=question[0]),
                    ]
                try:
                    response = chat(messages)
                    logger.info(response)
                    vul_dec = response.content
                    answers.append( [ v, vul_dec ])
                    qlist.append("\n ".join( question) )
                    time.sleep(3)
                except Exception as e:
                    logger.info(e)
                    continue

            with open(outputfile_answer, "w") as f1:
               text = [ a[1] for a in answers ]
               f1.write( "\n".join(text) )


def process_solidity_chat(project_folder, vul_folder, query_method, output_folder):
    pcode = parse_soldity_project( project_folder )
    prompt_tips = load_vul_examples(vul_folder, query_method)
    chat_gpt_answer(pcode, prompt_tips, output_folder, query_method)
    
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project", type=str, required=True, help="Project Folders")
    parser.add_argument("-c", "--checklist", type=str, default="datasets/solidity_vul/not-so-smart-contracts")
    parser.add_argument("-q", "--query",type=str, default="oneshot" )
    parser.add_argument("-o", "--output",type=str, default="tmp" )
    parser.add_argument("-l", "--max_len",type=int, default=1000 )
    args = parser.parse_args()
    chat = ChatOpenAI(temperature=0, max_tokens=args.max_len)
    process_solidity_chat(args.project, args.check, args.query, args.output)
   









    


