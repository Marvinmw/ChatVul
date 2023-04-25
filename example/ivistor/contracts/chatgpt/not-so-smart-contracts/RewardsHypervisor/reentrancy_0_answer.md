

### Vulnerability: Re-entrancy

The `withdraw` function in the `RewardsHypervisor` contract transfers tokens to the `to` address before burning the `shares` of the `from` address. This creates a potential re-entrancy vulnerability if the `to` address is a malicious contract that calls back into the `withdraw` function before the `shares` are burned.

To fix this vulnerability, the `shares` should be burned before transferring tokens to the `to` address.

```Solidity 
function withdraw(
    uint256 shares,
    address to,
    address payable from
) external returns (uint256 rewards) {
    require(shares > 0, "shares");
    require(to != address(0), "to");
    require(from != address(0), "from");
    require(from == msg.sender || IVisor(from).owner() == msg.sender, "Sender must own the tokens");
    rewards = visr.balanceOf(address(this)).mul(shares).div(vvisr.totalSupply());
    vvisr.burn(from, shares);
    visr.safeTransfer(to, rewards);
}
```