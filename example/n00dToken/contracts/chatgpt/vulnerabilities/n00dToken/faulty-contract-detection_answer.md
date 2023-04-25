

## Vulnerability Report

The code is vulnerable to the **Contract Initiated Calls** vulnerability.

### Description

The vulnerability arises from the fact that the contract does not check if the calling account has any code stored in it. This is a common way to prevent other contracts from interacting with the contract. However, contract accounts initiating calls during their construction will not yet show that they store code, effectively bypassing the contract detection.

### Example

The `n00dToken` contract inherits from the `ERC777` contract, which is vulnerable to the Contract Initiated Calls vulnerability. The `n00dToken` contract is created with an initial supply of tokens and an array of default operators. During the creation of the `n00dToken` contract, the `ERC777` constructor is called, which in turn calls the `_mint` function. This function is vulnerable to the Contract Initiated Calls vulnerability because it does not check if the calling account has any code stored in it.

### Recommendation

To fix this vulnerability, the contract should check if the calling account has any code stored in it before allowing the call to proceed. One way to do this is to use the `extcodesize` opcode, which returns the size of the code at the specified address. If the size is greater than zero, then the address is a contract and the call should be rejected.

### References

- [Solidity Documentation - Contract Creation](https://solidity.readthedocs.io/en/v0.8.7/contracts.html#contract-creation)
- [SWC-107: Reentrancy via Initialization](https://swcregistry.io/docs/SWC-107)