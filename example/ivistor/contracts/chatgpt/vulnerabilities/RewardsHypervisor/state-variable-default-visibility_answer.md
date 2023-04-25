

## Report

### State Variable Default Visibility

The code does not have any state variables, so there is no issue with default visibility.

### isContract Function

The `isContract` function is marked as private, which is good practice. However, it does not have the `view` modifier, which means that it modifies the state of the contract. Since this function does not actually modify the state, it should be marked as `view` to make it clear that it is a read-only function.

#### *Vulnerability Type: Incorrect Function Modifier*

#### *Status: Fixed*

#### *Fixed Code:*
```Solidity 
function isContract(address _addr) private view returns (bool isContract){
    uint32 size;
    assembly {
        size := extcodesize(_addr)
    }
    return (size > 0);
}
```