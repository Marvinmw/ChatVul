

## Report

### Floating Pragma

The smart contract uses a floating pragma `pragma solidity 0.7.6;`. This can be problematic as it allows the contract to be compiled with any version of the Solidity compiler greater than or equal to `0.7.6`. This can lead to issues if the contract is compiled with an outdated or buggy compiler version. It is recommended to use a fixed compiler version to ensure that the contract is compiled with a specific version of the compiler that has been thoroughly tested and considered for known bugs.

### isContract Function

The `isContract` function is used to check if an address is a contract or not. However, the function does not need to return a value, as the `size` variable is only used to check if the `extcodesize` of the address is greater than 0. Therefore, the function can be modified to return a boolean value directly, instead of returning the `size` variable.

```Solidity
function isContract(address _addr) private view returns (bool) {
    uint32 size;
    assembly {
        size := extcodesize(_addr)
    }
    return (size > 0);
}
```

### Conclusion

The smart contract has one potential vulnerability and one minor issue. The floating pragma can lead to issues if the contract is compiled with an outdated or buggy compiler version. The `isContract` function can be modified to return a boolean value directly, instead of returning the `size` variable.