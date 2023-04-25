

## Report
### Vulnerability Type: Write to Arbitrary Storage Location

The `deposit` function in the given smart contract is vulnerable to the Write to Arbitrary Storage Location attack. The function allows a user to deposit `visrDeposit` amount of tokens to the contract. The function calculates the number of shares to be minted based on the total supply of `vvisr` tokens and the balance of `visr` tokens in the contract. The function then transfers the `visrDeposit` amount of tokens from the `from` address to the contract. The `from` address can be a contract or an externally owned account. If the `from` address is a contract, the `delegatedTransferERC20` function of the `IVisor` interface is called to transfer the tokens. Otherwise, the `safeTransferFrom` function of the `visr` token is called to transfer the tokens.

The vulnerability in the `deposit` function is that it does not check the `from` address for any authorization requirements. An attacker can create a malicious contract that calls the `deposit` function with its own address as the `from` address. The `deposit` function will then transfer the `visrDeposit` amount of tokens from the malicious contract to the `to` address. The malicious contract can then overwrite its own storage variables to change its behavior or even take control of the contract.

### Recommendation

To fix the vulnerability, the `deposit` function should check the `from` address for authorization requirements. The function should only allow authorized addresses to deposit tokens to the contract. The function can use the `Ownable` contract to implement authorization requirements. The `deposit` function should also check that the `from` and `to` addresses are not the same as the contract address or the zero address.

```Solidity
function deposit(
    uint256 visrDeposit,
    address payable from,
    address to
) external onlyOwner returns (uint256 shares) {
    require(visrDeposit > 0, "deposits must be nonzero");
    require(to != address(0) && to != address(this), "to");
    require(from != address(0) && from != address(this), "from");
    shares = visrDeposit;
    if (vvisr.totalSupply() != 0) {
        uint256 visrBalance = visr.balanceOf(address(this));
        shares = shares.mul(vvisr.totalSupply()).div(visrBalance);
    }
    require(!isContract(from), "from must be an externally owned account");
    visr.safeTransferFrom(from, address(this), visrDeposit);
    vvisr.mint(to, shares);
}
```

The `isContract` function should also be updated to be a pure function since it does not modify the state of the contract.

```Solidity
function isContract(address _addr) private pure returns (bool isContract){
    uint32 size;
    assembly {
        size := extcodesize(_addr)
    }
    return (size > 0);
}
```