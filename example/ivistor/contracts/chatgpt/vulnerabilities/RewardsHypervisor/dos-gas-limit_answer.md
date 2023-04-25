

## Report

### Block Stuffing

The `deposit` function in the `RewardsHypervisor` contract can be vulnerable to block stuffing attack. The function calculates the number of shares to be minted based on the amount of `visrDeposit` received. If the `visr` balance of the contract is very low, then the calculation of shares can consume a lot of gas, and if an attacker sends a transaction with a very high gas price, they can fill up the block and prevent other transactions from being processed. 

### Vulnerability Type

Block Stuffing

### Vulnerable Function

```Solidity
function deposit(
    uint256 visrDeposit,
    address payable from,
    address to
) external returns (uint256 shares) {
    require(visrDeposit > 0, "deposits must be nonzero");
    require(to != address(0) && to != address(this), "to");
    require(from != address(0) && from != address(this), "from");
    shares = visrDeposit;
    if (vvisr.totalSupply() != 0) {
      uint256 visrBalance = visr.balanceOf(address(this));
      shares = shares.mul(vvisr.totalSupply()).div(visrBalance);
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

### Solution

To prevent block stuffing attacks, the `deposit` function should be modified to limit the amount of gas consumed in the calculation of shares. One way to do this is to set a maximum limit on the `visr` balance that can be used in the calculation. Another way is to split the calculation into multiple transactions, so that the gas consumption is spread out over multiple blocks. 

### Note

The `isContract` function can be improved by making it `view` and adding the `external` modifier. Also, the `IVisor` interface should be imported in the contract.