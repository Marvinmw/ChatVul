

## Report

### Integer Overflow and Underflow

The code does not contain any arithmetic operations that could result in integer overflow or underflow.

### Reentrancy

The code does not contain any external calls that could result in reentrancy attacks.

### Unchecked Return Value

The code uses the `safeTransfer` function from the `SafeERC20` library to transfer tokens, which checks the return value of the `transfer` function and reverts if it returns `false`. Therefore, there are no unchecked return values.

### Access Control

The code uses the `onlyOwner` modifier to restrict access to certain functions. However, the `isContract` function is not restricted and can be called by anyone. This could potentially be used to bypass the `if(isContract(from))` check in the `deposit` function and cause unexpected behavior.

### Unused Variables

The `owner` variable is unused and can be removed.

### Recommendation

Add an access control mechanism to the `isContract` function to restrict who can call it. For example, you could add a `onlyOwner` modifier to the function.

Remove the unused `owner` variable.

```Solidity 
pragma solidity 0.7.6;
import "./SafeMath.sol";
import "./ERC20.sol";
import "./IERC20.sol";
import "./SafeERC20.sol";
import "./Ownable.sol";
import "./IVisor.sol";
import "./vVISR.sol";
contract RewardsHypervisor {
    using SafeERC20 for IERC20;
    using SafeMath for uint256;
    IERC20 public visr;
    vVISR public vvisr;
    modifier onlyOwner {
        require(msg.sender == vvisr.owner(), "only owner");
        _;
    }
    constructor(
        address _visr,
        address _vvisr
    ) {
        visr = IERC20(_visr);
        vvisr = vVISR(_vvisr);
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
        if(isContract(from)) {
          IVisor(from).delegatedTransferERC20(address(visr), address(this), visrDeposit);
        }
        else {
          visr.safeTransferFrom(from, address(this), visrDeposit);
        }
        vvisr.mint(to, shares);
    }
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
    function snapshot() external onlyOwner {
      vvisr.snapshot();
    }
    function transferTokenOwnership(address newOwner) external onlyOwner {
      vvisr.transferOwnership(newOwner); 
    }
    function isContract(address _addr) private onlyOwner returns (bool isContract){
				uint32 size;
				assembly {
					size := extcodesize(_addr)
				}
				return (size > 0);
		}
}
```