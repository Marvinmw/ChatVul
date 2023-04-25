

### Vulnerability Report

#### TX.Origin Attack

In the `deposit` function, the `isContract` function is used to check if the `from` address is a contract or not. If it is a contract, then the `IVisor(from).delegatedTransferERC20` function is called to transfer the `visrDeposit` amount of tokens from the `from` address to the contract. However, this check is not sufficient to prevent a `tx.origin` attack as the `IVisor(from)` call can be made from a malicious contract that is called by the `tx.origin` address. This can result in the transfer of tokens from the `from` address to the malicious contract.

#### Unprotected Function

The `isContract` function is marked as private, but it is not marked as `view` or `pure`. This means that it can modify the state of the contract, which can lead to unexpected behavior. Since the function does not modify the state of the contract, it should be marked as `view`.

### Conclusion

The `deposit` function is vulnerable to a `tx.origin` attack, and the `isContract` function should be marked as `view`. 

#### Updated Code
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
    address public owner;
    IERC20 public visr;
    vVISR public vvisr;
    modifier onlyOwner {
        require(msg.sender == owner, "only owner");
        _;
    }
    constructor(
        address _visr,
        address _vvisr
    ) {
        visr = IERC20(_visr);
        vvisr = vVISR(_vvisr);
        owner = msg.sender;
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
          require(msg.sender == tx.origin, "Sender must be the original caller");
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
    function transferOwnership(address newOwner) external onlyOwner {
      owner = newOwner;
    }
    function transferTokenOwnership(address newOwner) external onlyOwner {
      vvisr.transferOwnership(newOwner); 
    }
    function isContract(address _addr) private view returns (bool isContract){
				uint32 size;
				assembly {
					size := extcodesize(_addr)
				}
				return (size > 0);
		}
}
```