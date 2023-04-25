## Delegatecall to Untrusted Callee

`Delegatecall` is a special variant of a message call. It is almost identical to a regular message call except the target address is executed in the context of the calling contract and `msg.sender` and `msg.value` remain the same. Essentially, `delegatecall` delegates other contracts to modify the calling contract's storage.

Since `delegatecall` gives so much control over a contract, it's very important to only use this with trusted contracts such as your own. If the target address comes from user input, be sure to verify that it is a trusted contract.

### Sources

- https://swcregistry.io/docs/SWC-112
- https://solidity.readthedocs.io/en/latest/introduction-to-smart-contracts.html#delegatecall-callcode-and-libraries
- https://blog.sigmaprime.io/solidity-security.html#delegatecall
- https://ethereum.stackexchange.com/questions/3667/difference-between-call-callcode-and-delegatecall