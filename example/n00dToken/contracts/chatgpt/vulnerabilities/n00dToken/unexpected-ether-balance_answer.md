

## Vulnerability Report

### Description

The smart contract code is vulnerable to the **Unexpected Ether Balance** vulnerability.

### Vulnerability Type

Unexpected Ether Balance

### Vulnerability Description

The smart contract assumes that there is no Ether balance in the contract. However, it is always possible to send Ether to a contract, and if a contract assumes a specific balance, it is vulnerable to attack. If a malicious user decides to exploit this by forcibly sending Ether, they will cause a DoS, rendering the contract unusable. For this reason, it's important to never use strict equality checks for the balance of Ether in a contract.

### Recommendation

To fix this vulnerability, the contract should not assume that there is no Ether balance in the contract. Instead, it should handle any Ether balance that is sent to the contract. One way to do this is to implement a fallback function that rejects any Ether sent to the contract. Another way is to use the `payable` modifier on a function that can receive Ether, and handle the Ether balance accordingly.

### References

- https://swcregistry.io/docs/SWC-132
- https://consensys.github.io/smart-contract-best-practices/attacks/denial-of-service/
- https://blog.sigmaprime.io/solidity-security.html#ether
- https://medium.com/@nmcl/gridlock-a-smart-contract-bug-73b8310608a9