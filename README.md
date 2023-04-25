## Introduction
This proejct is to utilize ChatGPT to detect the vulernability of Smart Contract in Solidity. It use *Apache Open license*.

## Set UP
- You need git submodule clone utils/tree-sitter-solidity, and then `cd utils && python build.py`
- environment `environment.yml`
  * `environment.yml` contains some packages related to cuda libraries and maybe you do not want them.
  * You need install the following packages, `langchain`, `python-dotenv`, `tree-sitter`, `tiktoken`, `openai`
- edit .env file and set your API Key, `OPENAI_API_KEY=YOUR_KEY_ID`

## Detection Model
    - tow types of prompt, `oneshot` and `concept`
        - `oneshot` needs the example code, 
            please see the folder `datasets/checklist/not-so-smart-contracts` and `datasets/checklist/ not-so-smart-contracts`.
            For example, [bad_randomness](datasets/checklist/not-so-smart-contracts/bad_randomness)
            - README.md describes the vul details.
            - *.sol files are the example code.
        - `concept` only needs the vul description, 
            please see the folder `datasets/checklist/smart-contract-vulnerabilities/vulnerabilities`
            each markdown file *.md contains one vul type details.
            For example, [arbitray-jump-function-type](datasets/checklist/smart-contract-vulnerabilities/vulnerabilities/arbitrary-jump-function-type.md)
    - We use the vul resouces from Github. Becasue we do not save the links, if you find your vul resouces are used by us, please touch me.

## Custom CheckList

If you want to add yourself checklist, you can 

    - create a parenet folder and then for each vul type, you can create a subfolder. 
    - In the subfolder, you describe the vul type. And if you want to use the example codel, please provide it in *.sol file. 

## Run commands

```
project_folder='example/ivistor/contracts' 
max_len=1000
python chatgpt_vul_dector.py -p ${project_folder} -c datasets/checklist/smart-contract-vulnerabilities/vulnerabilities -q concept -l ${max_len} -o ./tmp
python chatgpt_vul_dector.py -p ${project_folder} -c datasets/checklist/alchemy -l ${max_len}  -o ./tmp
python chatgpt_vul_dector.py -p ${project_folder} -c datasets/checklist/not-so-smart-contracts  -l ${max_len} -o ./tmp
```

The output is in `./tmp`


chatgpt_vul_dector, options
```Options
    -p, --project, "Project Folders"
    -c, --checklist, "Vulnerability List", plese see Detection Model section
    -q, --query , plese see Detection Model section
    -l, --maxlen , The maximum ouput length
    -o, --output , output folder
```



## Example

### 20211221 Visor Finance

#### Lost: $8.2 million

Testing

```sh
project_folder='example/ivistor/contracts' 
max_len=1000
python chatgpt_vul_dector.py -p ${project_folder} -c datasets/checklist/smart-contract-vulnerabilities/vulnerabilities -q concept -l ${max_len} -o example/ivistor/contracts/chatgpt
python chatgpt_vul_dector.py -p ${project_folder} -c datasets/checklist/alchemy -l ${max_len}  -o example/ivistor/contracts/chatgpt
python chatgpt_vul_dector.py -p ${project_folder} -c datasets/checklist/not-so-smart-contracts  -l ${max_len} -o example/ivistor/contracts/chatgpt
```

#### Contract

[RewardsHypervisor.sol](example/ivistor/contracts/RewardsHypervisor.sol)

### Reported by ChatVul

We list two reports realted to the real vulnerability exploied by the hacker. More details plase see the folder `example/ivistor/contracts/chatgpt`

[Detected Real Issue 1](example/ivistor/contracts/chatgpt/not-so-smart-contracts/RewardsHypervisor/denial_of_service_answer.md)
[Detected Real Issue 2](example/ivistor/contracts/chatgpt/alchemy/RewardsHypervisor/delegatecall_answer.md)

#### Vul Code

```RewardHypervisor.sol
    function deposit(
        uint256 visrDeposit,
        address payable from,
        address to
    ) external returns (uint256 shares) {
        require(visrDeposit > 0, "deposits must be nonzero");
        require(to != address(0) && to != address(this), "to");
        require(from != address(0) && from != address(this), "from");

        shares = visrDeposit;
        if (vvisr.totalSupply() != 0) {
          uint256 visrBalance = visr.balanceOf(address(this));
          shares = shares.mul(vvisr.totalSupply()).div(visrBalance);
        }

        if(isContract(from)) {
          require(IVisor(from).owner() == msg.sender); 
          IVisor(from).delegatedTransferERC20(address(visr), address(this), visrDeposit); // vulnerability position
        }
        else {
          visr.safeTransferFrom(from, address(this), visrDeposit);
        }

        vvisr.mint(to, shares);
    }
```


#### Link reference

https://beosin.medium.com/two-vulnerabilities-in-one-function-the-analysis-of-visor-finance-exploit-a15735e2492

https://twitter.com/GammaStrategies/status/1473306777131405314

https://etherscan.io/tx/0x69272d8c84d67d1da2f6425b339192fa472898dce936f24818fda415c1c1ff3f

---


### 20221026 N00d Token

#### Lost $29k

```sh
project_folder='example/n00dToken/contracts' 
max_len=1000
python chatgpt_vul_dector.py -p ${project_folder} -c datasets/checklist/smart-contract-vulnerabilities/vulnerabilities -q concept -l ${max_len} -o example/n00dToken/contracts/chatgpt
python chatgpt_vul_dector.py -p ${project_folder} -c datasets/checklist/alchemy -l ${max_len}  -o example/n00dToken/contracts/chatgpt
python chatgpt_vul_dector.py -p ${project_folder} -c datasets/checklist/not-so-smart-contracts  -l ${max_len} -o example/n00dToken/contracts/chatgpt
```

#### Contract

[n00dToken.sol](example/n00dToken/contracts/n00dToken.sol)

### Reported by ChatVul

We list two reports realted to the real vulnerability exploied by the hacker. More details plase see the folder `example/n00dToken/contracts/chatgpt`

[Detected Real Issue 1](example/n00dToken/contracts/chatgpt/not-so-smart-contracts/n00dToken/honeypost_GiftBox_answer.md)
[Detected Real Issue 2](example/n00dToken/contracts/chatgpt/vulnerabilities/n00dToken/arbitrary-jump-function-type_answer.md)

#### Vul Code

```entrance point
    function transfer(address recipient, uint256 amount) public virtual override returns (bool) {
        _send(_msgSender(), recipient, amount, "", "", false);
        return true;
    }
```

```vulnerability position
 function _send(
        address from,
        address to,
        uint256 amount,
        bytes memory userData,
        bytes memory operatorData,
        bool requireReceptionAck
    ) internal virtual {
        require(from != address(0), "ERC777: transfer from the zero address");
        require(to != address(0), "ERC777: transfer to the zero address");

        address operator = _msgSender();

        _callTokensToSend(operator, from, to, amount, userData, operatorData);

        _move(operator, from, to, amount, userData, operatorData);

        _callTokensReceived(operator, from, to, amount, userData, operatorData, requireReceptionAck);
    }

    function _callTokensToSend(
        address operator,
        address from,
        address to,
        uint256 amount,
        bytes memory userData,
        bytes memory operatorData
    ) private {
        address implementer = _ERC1820_REGISTRY.getInterfaceImplementer(from, _TOKENS_SENDER_INTERFACE_HASH); // here
        if (implementer != address(0)) {
            IERC777Sender(implementer).tokensToSend(operator, from, to, amount, userData, operatorData); // here
        }
    }
```

#### Link reference

https://twitter.com/BlockSecTeam/status/1584959295829180416

https://twitter.com/AnciliaInc/status/1584955717877784576


## To DO
Since the project is still in its early stages, it is crucial to determine how to extract the context for a large project that involves static and dynamic analysis. We welcome any feedback or suggestions on this matter and encourage you to get in touch with us via email or pull request on our GitHub repository. Your input will be valuable in enhancing the effectiveness of the project.
