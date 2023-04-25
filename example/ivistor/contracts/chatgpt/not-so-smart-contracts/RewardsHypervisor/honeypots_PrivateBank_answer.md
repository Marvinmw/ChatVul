

## Report

### Integer Overflow and Underflow

#### `deposit` function

In the `deposit` function, the following line of code can cause an integer overflow if `visrBalance` is less than `visrDeposit`:

```solidity
shares = shares.mul(vvisr.totalSupply()).div(visrBalance);
```

If `visrBalance` is less than `visrDeposit`, then `shares` will be greater than `visrDeposit` and an integer overflow will occur. This can be fixed by checking if `visrBalance` is greater than or equal to `visrDeposit` before performing the calculation.

#### `withdraw` function

In the `withdraw` function, the following line of code can cause an integer underflow if `vvisr.totalSupply()` is less than `shares`:

```solidity
rewards = visr.balanceOf(address(this)).mul(shares).div(vvisr.totalSupply());
```

If `vvisr.totalSupply()` is less than `shares`, then `rewards` will be greater than the balance of `visr` held by the contract, causing an integer underflow. This can be fixed by checking if `vvisr.totalSupply()` is greater than or equal to `shares` before performing the calculation.

### Unchecked Return Value

#### `withdraw` function

In the `withdraw` function, the following line of code calls the `safeTransfer` function from the `visr` contract:

```solidity
visr.safeTransfer(to, rewards);
```

The `safeTransfer` function returns a boolean value indicating whether the transfer was successful or not, but this return value is not checked. This can result in the loss of funds if the transfer fails. To fix this, the return value of `safeTransfer` should be checked and appropriate action taken if the transfer fails.

### Private Function Not Marked as View

#### `isContract` function

The `isContract` function is a private function that is used to check if an address is a contract or not. However, this function does not modify the state of the contract and should be marked as `view` to indicate this. Marking the function as `view` will make it clear that the function does not modify the state of the contract and will also allow the function to be called from other `view` or `pure` functions.

### Conclusion

The new smart contract code has three potential vulnerabilities: integer overflow and underflow, unchecked return value, and a private function not marked as `view`. The integer overflow and underflow vulnerabilities can be fixed by checking if the divisor is greater than or equal to the dividend before performing the calculation. The unchecked return value vulnerability can be fixed by checking the return value of the `safeTransfer` function. The `isContract` function should be marked as `view` to indicate that it does not modify the state of the contract.