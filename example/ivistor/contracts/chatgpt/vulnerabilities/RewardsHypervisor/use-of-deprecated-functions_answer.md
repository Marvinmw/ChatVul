

## Report

### Vulnerability Type: Use of Deprecated Functions

### Vulnerable Function(s)
The following deprecated functions are used in the smart contract:
- `safeTransferFrom` from `SafeERC20.sol`
- `safeTransfer` from `SafeERC20.sol`

### Details
The `safeTransferFrom` and `safeTransfer` functions from the `SafeERC20` library are deprecated and have been replaced with `transferFrom` and `transfer` functions respectively. Using deprecated functions can lead to unexpected effects and compilation errors.

### Recommendation
The `safeTransferFrom` and `safeTransfer` functions should be replaced with `transferFrom` and `transfer` functions respectively to avoid any potential issues.