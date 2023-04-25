

## Report

### Vulnerability Type: 
Unprotected Contract State Modification

### Vulnerability Description:
The `isContract` function is used to check if the `from` address is a contract or not. If it is a contract, the `deposit` function calls the `delegatedTransferERC20` function of the `IVisor` contract to transfer the `visrDeposit` amount of tokens to the `RewardsHypervisor` contract. However, the `isContract` function does not have the `view` modifier, which means that it modifies the contract state. This can cause issues when the `deposit` function is called during the contract's construction, as the `isContract` function will return `false` even if the `from` address is a contract. This can allow malicious contracts to bypass the contract detection and interact with the `RewardsHypervisor` contract.

### Recommendation:
To fix this vulnerability, the `isContract` function should have the `view` modifier to ensure that it does not modify the contract state. The updated function should look like this:

```Solidity
function isContract(address _addr) private view returns (bool isContract){
    uint32 size;
    assembly {
        size := extcodesize(_addr)
    }
    return (size > 0);
}
```

### Reference:
- [Solidity Documentation - View Functions](https://solidity.readthedocs.io/en/v0.8.7/contracts.html#view-functions)