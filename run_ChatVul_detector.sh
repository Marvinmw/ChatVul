#!/bin/bash
echo "Start Scan Give Files"
project_folder=$1
max_len=$2
output=$3
if [ -d ${project_folder} ]; then
    python chatgpt_vul_dector.py -p ${project_folder} -c datasets/checklist/smart-contract-vulnerabilities/vulnerabilities -q concept -l ${max_len} -o ${output}
    python chatgpt_vul_dector.py -p ${project_folder} -c datasets/checklist/alchemy -l ${max_len} -o ${output}
    python chatgpt_vul_dector.py -p ${project_folder} -c datasets/checklist/not-so-smart-contracts  -l ${max_len} -o ${output}
else
    echo "Folder does not exist"
fi


