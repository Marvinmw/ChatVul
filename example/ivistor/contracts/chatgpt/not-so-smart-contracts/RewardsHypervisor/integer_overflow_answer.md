

## Report

### Integer Overflow

The new smart contract code does not contain any arithmetic operations that could lead to integer overflow vulnerabilities. Therefore, there is no risk of integer overflow in this contract.

### Unprotected Function

The `isContract` function in the new smart contract code is not marked as `view` or `pure`, even though it does not modify the state of the contract. This means that it consumes gas when called, which could be used to perform a denial-of-service attack on the contract. To fix this issue, the `isContract` function should be marked as `view`.

Vulnerable function:

```Solidity
function isContract(address _addr) private returns (bool isContract){
    uint32 size;
    assembly {
        size := extcodesize(_addr)
    }
    return (size > 0);
}
```

Fixed function:

```Solidity
function isContract(address _addr) private view returns (bool isContract){
    uint32 size;
    assembly {
        size := extcodesize(_addr)
    }
    return (size > 0);
}
```

### Reentrancy

The `withdraw` function in the new smart contract code is vulnerable to reentrancy attacks. An attacker could create a malicious contract that calls the `withdraw` function repeatedly before the first call completes, allowing them to drain the contract's balance. To fix this issue, the contract should use the "checks-effects-interactions" pattern to ensure that all state changes are made before any external calls are made.

Vulnerable function:

```Solidity
function withdraw(
    uint256 shares,
    address to,
    address payable from
) external returns (uint256 rewards) {
    require(shares > 0, "shares");
    require(to != address(0), "to");
    require(from != address(0), "from");
    rewards = visr.balanceOf(address(this)).mul(shares).div(vvisr.totalSupply());
    visr.safeTransfer(to, rewards);
    require(from == msg.sender || IVisor(from).owner() == msg.sender, "Sender must own the tokens");
    vvisr.burn(from, shares);
}
```

Fixed function:

```Solidity
function withdraw(
    uint256 shares,
    address to,
    address payable from
) external returns (uint256 rewards) {
    require(shares > 0, "shares");
    require(to != address(0), "to");
    require(from != address(0), "from");
    uint256 visrBalance = visr.balanceOf(address(this));
    rewards = visrBalance.mul(shares).div(vvisr.totalSupply());
    vvisr.burn(from, shares);
    visr.safeTransfer(to, rewards);
    require(from == msg.sender || IVisor(from).owner() == msg.sender, "Sender must own the tokens");
}
```

In the fixed function, the `vvisr.burn` function is called before the `visr.safeTransfer` function, ensuring that all state changes are made before any external calls are made.

### Conclusion

The new smart contract code is vulnerable to reentrancy attacks in the `withdraw` function and has an unprotected function in the `isContract` function. These issues can be fixed by using the "checks-effects-interactions" pattern in the `withdraw` function and marking the `isContract` function as `view`.