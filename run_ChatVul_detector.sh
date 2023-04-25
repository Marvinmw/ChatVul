#!/bin/bash
echo "Start Scan Give Files"
project_folder=$1
max_len=$2
if [ -d ${project_folder} ]; then
    python chatgpt_vul_dector.py -p ${project_folder} -c datasets/solidity_vul/smart-contract-vulnerabilities/vulnerabilities -q concept -l ${max_len}
    python chatgpt_vul_dector.py -p ${project_folder} -c datasets/solidity_vul/alchemy -l ${max_len}
    python chatgpt_vul_dector.py -p ${project_folder} -c datasets/solidity_vul/not-so-smart-contracts  -l ${max_len}
else
    echo "Folder does not exist"
fi


