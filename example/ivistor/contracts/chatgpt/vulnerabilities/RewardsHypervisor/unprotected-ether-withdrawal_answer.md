

## Report

### Unprotected Ether Withdrawal

The provided smart contract code is not vulnerable to the Unprotected Ether Withdrawal vulnerability. This vulnerability is related to the possibility of a bad actor being able to withdraw some or all Ether from a contract due to misnaming a function intended to be a constructor, giving anyone access to re-initialize the contract. However, this contract does not have any function that allows the withdrawal of Ether, and the constructor is named correctly.

### Other Issues

The `isContract` function is not marked as `view`, even though it does not modify the state of the contract. This can lead to unnecessary gas consumption when calling this function.

To fix this issue, the `isContract` function should be marked as `view`.

### Recommendation

Mark the `isContract` function as `view` to avoid unnecessary gas consumption.

```Solidity
function isContract(address _addr) private view returns (bool isContract){
    uint32 size;
    assembly {
        size := extcodesize(_addr)
    }
    return (size > 0);
}
```