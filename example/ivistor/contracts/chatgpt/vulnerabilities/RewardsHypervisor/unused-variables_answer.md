

## Vulnerability Type: Presence of Unused Variables

The `owner` variable is declared but not used in the smart contract. This can lead to an increase in computations (unnecessary gas consumption), indication of bugs or malformed data structures, and decreased code readability. It is recommended to remove all unused variables from a code base.

### Source

- https://swcregistry.io/docs/SWC-131
- https://github.com/ethereum/solidity/issues/718
- https://github.com/ethereum/solidity/issues/2563