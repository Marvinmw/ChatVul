

## Report

### Assert Violation

#### Description

The `deposit` function in the `RewardsHypervisor` contract uses an `if` statement to check if the `totalSupply` of `vvisr` is not equal to zero. If it is not zero, it calculates the `shares` by dividing the `visrDeposit` by the `visrBalance` and multiplying it by the `totalSupply` of `vvisr`. However, if the `totalSupply` of `vvisr` is zero, the `shares` variable is not updated and remains equal to `visrDeposit`. This can lead to a division by zero error in the next line of code, which will cause the transaction to revert.

#### Recommendation

To fix this issue, the `shares` variable should be initialized to zero before the `if` statement. This will ensure that the `shares` variable is always defined, even if the `totalSupply` of `vvisr` is zero.

#### Example

```Solidity
function deposit(
    uint256 visrDeposit,
    address payable from,
    address to
) external returns (uint256 shares) {
    require(visrDeposit > 0, "deposits must be nonzero");
    require(to != address(0) && to != address(this), "to");
    require(from != address(0) && from != address(this), "from");
    shares = 0;
    if (vvisr.totalSupply() != 0) {
        uint256 visrBalance = visr.balanceOf(address(this));
        shares = visrDeposit.mul(vvisr.totalSupply()).div(visrBalance);
    }
    if(isContract(from)) {
        IVisor(from).delegatedTransferERC20(address(visr), address(this), visrDeposit);
    }
    else {
        visr.safeTransferFrom(from, address(this), visrDeposit);
    }
    vvisr.mint(to, shares);
}
```