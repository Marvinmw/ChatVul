

Vulnerability Type: Uninitialized Storage Pointer

In the `deposit` function, the `isContract` function is called to check if the `from` address is a contract. However, the `isContract` function does not have the `view` modifier, and it writes to storage by using assembly code to check the size of the contract code at the given address. This causes the `isContract` function to act like a storage pointer, which can be used to overwrite storage variables. 

To fix this vulnerability, the `isContract` function should have the `view` modifier to ensure that it does not write to storage. 

Fixed code:
```Solidity 
function isContract(address _addr) private view returns (bool isContract){
    uint32 size;
    assembly {
        size := extcodesize(_addr)
    }
    return (size > 0);
}
```