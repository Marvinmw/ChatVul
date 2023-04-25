

## Report
### Vulnerability Type: Reentrancy

The `withdraw` function in the `RewardsHypervisor` contract is vulnerable to reentrancy attacks. The function first calculates the amount of rewards to be transferred to the `to` address based on the number of `shares` being withdrawn. Then, it transfers the rewards to the `to` address using the `safeTransfer` function from the `visr` token contract. However, before the transfer is complete, the function calls the `burn` function of the `vVISR` contract, which can call back into the `RewardsHypervisor` contract and execute the `withdraw` function again before the transfer is complete. This can result in the attacker receiving more rewards than they are entitled to.

### Recommendation

To prevent reentrancy attacks, the `withdraw` function should be modified to follow the checks-effects-interactions pattern. The function should first calculate the amount of rewards to be transferred and store it in a local variable. Then, it should update the state variables to reflect the withdrawal. Finally, it should transfer the rewards to the `to` address. This will ensure that the transfer is completed before any other function is called.

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
    vvisr.burn(from, shares);
    visr.safeTransfer(to, rewards);
    require(from == msg.sender || IVisor(from).owner() == msg.sender, "Sender must own the tokens");
}
```