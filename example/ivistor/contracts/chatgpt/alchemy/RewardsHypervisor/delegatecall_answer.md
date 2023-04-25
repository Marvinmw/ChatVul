

## Report

### Vulnerability

The `deposit` function in the `RewardsHypervisor` contract is vulnerable to a delegate call attack.

### Description

The `deposit` function calls the `isContract` function to check if the `from` address is a contract or not. If it is a contract, the function calls the `delegatedTransferERC20` function of the `IVisor` contract to transfer the `visrDeposit` tokens to the `RewardsHypervisor` contract. The `delegatedTransferERC20` function is called using a delegate call, which means that the `IVisor` contract's code is executed in the context of the `RewardsHypervisor` contract, and the `IVisor` contract's storage is used instead of the `RewardsHypervisor` contract's storage.

This can be exploited by an attacker who deploys a malicious contract that implements the `IVisor` interface and overrides the `delegatedTransferERC20` function to perform arbitrary actions, such as stealing tokens or modifying the `RewardsHypervisor` contract's storage.

### Recommendation

To fix this vulnerability, the `deposit` function should not use a delegate call to call the `delegatedTransferERC20` function. Instead, it should call the function directly using a regular message call. This will ensure that the `IVisor` contract's code is executed in its own context, and its storage is not affected by the `RewardsHypervisor` contract.

```Solidity
if(isContract(from)) {
  IVisor(from).delegatedTransferERC20(address(visr), address(this), visrDeposit);
}
else {
  visr.safeTransferFrom(from, address(this), visrDeposit);
}
```

should be replaced with:

```Solidity
if(isContract(from)) {
  require(IVisor(from).delegatedTransferERC20(address(visr), address(this), visrDeposit), "delegated transfer failed");
}
else {
  visr.safeTransferFrom(from, address(this), visrDeposit);
}
```

### References

- [Solidity Documentation - Delegatecall](https://solidity.readthedocs.io/en/v0.8.7/introduction-to-smart-contracts.html#delegatecall-callcode-and-libraries)
- [OpenZeppelin - Delegatecall to Untrusted Callee](https://blog.openzeppelin.com/delegatecall-to-untrusted-contracts/)
- [SWC-112 - Delegatecall to Untrusted Callee](https://swcregistry.io/docs/SWC-112)