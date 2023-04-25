## Vulnerability Report

The code is vulnerable to the **Asserting EOA from Code Size** vulnerability.

### Description

The `isContract` function is used to check if the `from` address is a contract or an EOA. However, this function uses the `extcodesize` opcode to check the size of the code at the given address. This is the same method that was recently discovered to be exploitable. An attacker can create a contract that has no code, but when called, it will return a non-zero code size. This can cause the `isContract` function to return `true` for an EOA, leading to unexpected behavior in the contract.

### Recommendation

To fix this vulnerability, the contract should use a different method to check if an address is a contract or an EOA. One possible method is to use the `balance` property of the address. If the balance is zero, then it is an EOA, otherwise, it is a contract. Another method is to use the `codehash` property of the address. If the `codehash` is zero, then it is an EOA, otherwise, it is a contract.

### Example

Here is an example of how to use the `balance` property to check if an address is a contract or an EOA:

```solidity
function isContract(address _addr) private view returns (bool) {
    uint256 balance = _addr.balance;
    return balance > 0;
}
```

Here is an example of how to use the `codehash` property to check if an address is a contract or an EOA:

```solidity
function isContract(address _addr) private view returns (bool) {
    bytes32 codehash;
    assembly { codehash := extcodehash(_addr) }
    return codehash != 0x0;
}
```

Note that the `codehash` property is only available in Solidity version 0.5.0 or later.