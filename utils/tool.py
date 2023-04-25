
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
from io import StringIO
import time
import  tokenize
import re
from tree_sitter import Language, Parser
import re
from io import StringIO
import  tokenize
import os
lang="solidity"
parsers={}        
LANGUAGE = Language(f'{os.getcwd()}/utils/my-languages.so', lang)
solidity_parser = Parser()
solidity_parser.set_language(LANGUAGE)   
parsers[lang]= solidity_parser


def split_functions(code):
   # print(type(code))
    tree = solidity_parser.parse(bytes(f"""{code}""",'utf8'))  
   
    code=code.split('\n')
 

    query = LANGUAGE.query("""
    (function_definition
      name: (identifier) @function.def)
    """)
   
    captures = query.captures(tree.root_node)
    res = {}
    for fdef in captures:
        node=fdef[0].parent
        fncode = []
        for child_node in node.children:
            sp = child_node.start_point
            ep = child_node.end_point   
            ct = index_to_code_token((sp, ep), code)
            fncode.append( ct  )
        res[fncode[1]]=" ".join(fncode)
    
     # constructor_definition
    query1 = LANGUAGE.query("""
    (constructor_definition  "constructor" @constructor)
    """)
    captures = query1.captures(tree.root_node)
    for fdef in captures:
        node=fdef[0].parent
        fncode = []
        for child_node in node.children:
            sp = child_node.start_point
            ep = child_node.end_point   
            ct = index_to_code_token((sp, ep), code)
            fncode.append( ct  )
        res[fncode[0]]=" ".join(fncode)
    return res
    

def remove_comments_and_docstrings(source,lang="solidity"):
    if lang in ['python']:
        """
        Returns 'source' minus comments and docstrings.
        """
        io_obj = StringIO(source)
        out = ""
        prev_toktype = tokenize.INDENT
        last_lineno = -1
        last_col = 0
        for tok in tokenize.generate_tokens(io_obj.readline):
            token_type = tok[0]
            token_string = tok[1]
            start_line, start_col = tok[2]
            end_line, end_col = tok[3]
            ltext = tok[4]
            if start_line > last_lineno:
                last_col = 0
            if start_col > last_col:
                out += (" " * (start_col - last_col))
            # Remove comments:
            if token_type == tokenize.COMMENT:
                pass
            # This series of conditionals removes docstrings:
            elif token_type == tokenize.STRING:
                if prev_toktype != tokenize.INDENT:
            # This is likely a docstring; double-check we're not inside an operator:
                    if prev_toktype != tokenize.NEWLINE:
                        if start_col > 0:
                            out += token_string
            else:
                out += token_string
            prev_toktype = token_type
            last_col = end_col
            last_lineno = end_line
        temp=[]
        for x in out.split('\n'):
            if x.strip()!="":
                temp.append(x)
        return '\n'.join(temp)
    elif lang in ['ruby']:
        return source
    else:
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return " " # note: a space and not an empty string
            else:
                return s
        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        temp=[]
        for x in re.sub(pattern, replacer, source).split('\n'):
            if x.strip()!="":
                temp.append(x)
        return '\n'.join(temp)

# def tree_to_token_index(root_node):
#     if (len(root_node.children)==0 or root_node.type=='string') and root_node.type!='comment':
#         return [(root_node.start_point,root_node.end_point)]
#     else:
#         code_tokens=[]
#         for child in root_node.children:
#             code_tokens+=tree_to_token_index(child)
#         return code_tokens

def tree_to_token_index(root_node):
    '''
    return a list that contains [ (node position, node type, node parent type) ]
    '''
    if (len(root_node.children)==0 or root_node.type=='string') and root_node.type!='comment':
        return [(root_node.start_point, root_node.end_point, root_node.type, root_node.parent.type)]
    else:
        code_tokens=[]
        for child in root_node.children:
            code_tokens+=tree_to_token_index(child)
        return code_tokens

def index_to_code_dic(tokens_index, code_tokens):
    '''
    return a dict that contains { node_position (start_point, end_point): ( node_position, code_span ) }
    '''
    index_to_code={}
    for idx,(index,code) in enumerate(zip(tokens_index,code_tokens)):
            index_to_code[index]=(idx,code) 
    return index_to_code
    
def tree_to_variable_index(root_node,index_to_code):
    '''
    return a list variables 
    '''
    if (len(root_node.children)==0 or root_node.type=='string') and root_node.type!='comment':
        index=(root_node.start_point,root_node.end_point)
        _,code=index_to_code[index]
        if root_node.type!=code:
            return [(root_node.start_point,root_node.end_point)]
        else:
            return []
    else:
        code_tokens=[]
        for child in root_node.children:
            code_tokens+=tree_to_variable_index(child,index_to_code)
        return code_tokens    

def index_to_code_token(index,code):
    '''
    return the piece of code accroding to the node index
    '''
    start_point=index[0]
    end_point=index[1]
    if start_point[0]==end_point[0]:
        s=code[start_point[0]][start_point[1]:end_point[1]]
    else:
        s=""
        s+=code[start_point[0]][start_point[1]:]
        for i in range(start_point[0]+1,end_point[0]):
            s+=code[i]
        s+=code[end_point[0]][:end_point[1]]   
    return s

