

## Vulnerability Report

### Floating Pragma

Severity: **Low**

### Description

The contract uses a floating pragma, which allows the use of any version of the Solidity compiler greater than or equal to version 0.8.0. This can lead to issues if the contract is deployed using an outdated or problematic compiler version, which can cause bugs and put the contract's security at risk.

### Recommendation

It is recommended to use a fixed pragma instead of a floating pragma. This will ensure that the contract is compiled using a specific version of the Solidity compiler, which has been thoroughly tested and considered for known bugs. 

### References

- https://swcregistry.io/docs/SWC-103
- https://consensys.github.io/smart-contract-best-practices/development-recommendations/solidity-specific/locking-pragmas/