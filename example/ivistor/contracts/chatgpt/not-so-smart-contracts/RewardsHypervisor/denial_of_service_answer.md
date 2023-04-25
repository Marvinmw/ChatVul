

Vulnerability Type: Reentrancy Attack

The `deposit` function in the `RewardsHypervisor` contract is vulnerable to a reentrancy attack. If `from` is a malicious contract that calls back into the `RewardsHypervisor` contract during the execution of the `deposit` function, it can cause the function to be executed multiple times before the first execution completes, leading to unexpected behavior and potential loss of funds.

Explanation:

The `deposit` function first checks if `from` is a contract by calling the `isContract` function. If `from` is a contract, it calls the `delegatedTransferERC20` function on the `IVisor` interface, which can be implemented by any contract. This function can potentially call back into the `RewardsHypervisor` contract, leading to a reentrancy attack.

Mitigation:

To prevent reentrancy attacks, the `deposit` function should use the `nonReentrant` modifier from the OpenZeppelin library, which prevents a function from being called again until the previous call has completed. Additionally, the `isContract` function should be updated to be `pure` instead of `private` to prevent any potential state changes.

Fixed Code:

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
    modifier nonReentrant() {
        require(!_reentrant, "Reentrant call");
        _reentrant = true;
        _;
        _reentrant = false;
    }
    bool private _reentrant = false;
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
    ) external nonReentrant returns (uint256 shares) {
        require(visrDeposit > 0, "deposits must be nonzero");
        require(to != address(0) && to != address(this), "to");
        require(from != address(0) && from != address(this), "from");
        require(!isContract(from), "from cannot be a contract");
        shares = visrDeposit;
        if (vvisr.totalSupply() != 0) {
          uint256 visrBalance = visr.balanceOf(address(this));
          shares = shares.mul(vvisr.totalSupply()).div(visrBalance);
        }
        visr.safeTransferFrom(from, address(this), visrDeposit);
        vvisr.mint(to, shares);
    }
    function withdraw(
        uint256 shares,
        address to,
        address payable from
    ) external nonReentrant returns (uint256 rewards) {
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
    function isContract(address _addr) public pure returns (bool isContract){
				uint32 size;
				assembly {
					size := extcodesize(_addr)
				}
				return (size > 0);
		}
}
```