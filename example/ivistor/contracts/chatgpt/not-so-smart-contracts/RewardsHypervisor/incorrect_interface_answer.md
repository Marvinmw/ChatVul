

Vulnerability Type: Incorrect interface

In the `deposit` function, there is a call to `IVisor(from).delegatedTransferERC20`, which assumes that the `from` address is a contract that implements the `IVisor` interface. However, there is no check to ensure that this is the case, and if the `from` address is not a contract that implements the `IVisor` interface, the call will fail and the transaction will revert.

To fix this vulnerability, the `isContract` function should be updated to return a boolean value and made `pure` to avoid modifying the state. Additionally, a check should be added to ensure that the `from` address is a contract that implements the `IVisor` interface before making the call to `delegatedTransferERC20`.

Fixed code:
```Solidity 
function isContract(address _addr) private view returns (bool) {
    uint32 size;
    assembly {
        size := extcodesize(_addr)
    }
    return (size > 0);
}

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
    if (isContract(from)) {
        require(
            IVisor(from).supportsInterface(
                type(IVisor).interfaceId
            ),
            "from must implement IVisor"
        );
        IVisor(from).delegatedTransferERC20(
            address(visr),
            address(this),
            visrDeposit
        );
    } else {
        visr.safeTransferFrom(from, address(this), visrDeposit);
    }
    vvisr.mint(to, shares);
}
```