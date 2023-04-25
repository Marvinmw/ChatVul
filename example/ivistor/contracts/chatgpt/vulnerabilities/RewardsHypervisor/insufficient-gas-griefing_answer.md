## Report

### Vulnerability Type: Insufficient Gas Griefing

The `deposit` function in the `RewardsHypervisor` contract is vulnerable to an Insufficient Gas Griefing attack. The function accepts a `visrDeposit` parameter, which is used to calculate the number of `shares` to mint for the `to` address. The function then transfers the `visrDeposit` from the `from` address to the contract using `visr.safeTransferFrom(from, address(this), visrDeposit)`. 

An attacker can call the `deposit` function with a `from` address that is a contract that will revert when the `delegatedTransferERC20` function is called. The attacker can set the gas limit for the transaction to just enough to execute the `deposit` function, but not enough to execute the `delegatedTransferERC20` function. This will cause the `deposit` function to fail, but the transaction will still be considered successful, and the attacker will have effectively censored the transaction.

### Recommendation

To prevent Insufficient Gas Griefing attacks, the `deposit` function should require that the `from` address is not a contract. Alternatively, the function should require that the `msg.sender` is a trusted relayer that has provided enough gas for the transaction to succeed.