## Report

### Vulnerability Type
Unchecked Call Return Value

### Vulnerability Description
The `deposit` function calls the `delegatedTransferERC20` function of the `IVisor` contract without checking the return value. If the `delegatedTransferERC20` function fails, the `deposit` function will continue to execute, leading to unexpected behavior and breaking the program logic. An attacker can exploit this vulnerability to cause further damage to the application.

### Recommendation
The return value of the `delegatedTransferERC20` function should be checked to ensure that the transfer was successful. If the transfer fails, the `deposit` function should revert the transaction and return an error message to the user.

### Reference
- https://swcregistry.io/docs/SWC-104
- https://consensys.github.io/smart-contract-best-practices/development-recommendations/general/external-calls/