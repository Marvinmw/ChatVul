

## Vulnerability Report

The code seems to be free of any vulnerabilities related to the provided vulnerability details. However, there is one issue that can be improved:

### isContract Function

The `isContract` function is not marked as `view` even though it does not modify the state. This can cause unnecessary gas consumption when calling this function. Therefore, it is recommended to mark it as `view`.

#### Recommendation

Add the `view` modifier to the `isContract` function as follows:

```Solidity
function isContract(address _addr) private view returns (bool isContract){
    uint32 size;
    assembly {
        size := extcodesize(_addr)
    }
    return (size > 0);
}
```

## Conclusion

The code is safe from the provided vulnerability details. However, the `isContract` function can be improved by adding the `view` modifier.