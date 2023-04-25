

## Report
### Denial of Service (DoS) with Revert

The `deposit` function in the `RewardsHypervisor` contract is vulnerable to a DoS attack with revert. The function transfers `visrDeposit` amount of `visr` tokens from `from` address to the contract address and mints `shares` amount of `vvisr` tokens to the `to` address. If `from` address is a contract, the `delegatedTransferERC20` function of the `IVisor` interface is called to transfer the tokens. Otherwise, the `safeTransferFrom` function of the `visr` token is called to transfer the tokens. 

The problem with this implementation is that if the `from` address is a malicious contract that reverts the transaction, the entire `deposit` function will revert, and the tokens will not be transferred to the contract address. This will prevent any further deposits to the contract, and the users will not be able to earn rewards. 

To mitigate this vulnerability, the contract should use a pull payment system instead of a push payment system. In a pull payment system, the users should call a function to withdraw their rewards instead of the contract pushing the rewards to the users. This way, the users will have control over the transaction, and the contract will not be vulnerable to a DoS attack with revert.

### Recommendation

To fix the vulnerability, the contract should implement a pull payment system where the users can withdraw their rewards by calling a function. The `deposit` function should only transfer the tokens to the contract address and mint the `vvisr` tokens to the `to` address. The `withdraw` function should be modified to allow the users to withdraw their rewards by burning their `vvisr` tokens and transferring the corresponding amount of `visr` tokens to their address. 

```Solidity
function deposit(
    uint256 visrDeposit,
    address to
) external returns (uint256 shares) {
    require(visrDeposit > 0, "deposits must be nonzero");
    require(to != address(0) && to != address(this), "to");
    shares = visrDeposit;
    if (vvisr.totalSupply() != 0) {
        uint256 visrBalance = visr.balanceOf(address(this));
        shares = shares.mul(vvisr.totalSupply()).div(visrBalance);
    }
    visr.safeTransferFrom(msg.sender, address(this), visrDeposit);
    vvisr.mint(to, shares);
}

function withdraw() external {
    uint256 shares = vvisr.balanceOf(msg.sender);
    require(shares > 0, "no shares to withdraw");
    uint256 rewards = visr.balanceOf(address(this)).mul(shares).div(vvisr.totalSupply());
    vvisr.burn(msg.sender, shares);
    visr.safeTransfer(msg.sender, rewards);
}
```

In the modified implementation, the `deposit` function only transfers the tokens to the contract address and mints the `vvisr` tokens to the `to` address. The `withdraw` function allows the users to withdraw their rewards by burning their `vvisr` tokens and transferring the corresponding amount of `visr` tokens to their address. The `withdraw` function does not take any arguments, and the tokens are transferred to the address of the caller. 

Note that the `isContract` function is not used in the modified implementation and can be removed.