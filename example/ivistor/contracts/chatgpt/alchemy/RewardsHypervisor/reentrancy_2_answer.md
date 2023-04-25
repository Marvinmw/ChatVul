

### Vulnerability Report

#### Reentrancy Attack

The new smart contract code does not have any direct reentrancy vulnerability. However, it does have a function `isContract` that can be used to check if an address is a contract or not. This function can be used to perform a reentrancy attack if it is called with an external contract address that has a fallback function that calls back into the `RewardsHypervisor` contract.

An attacker can create a malicious contract with a fallback function that calls the `isContract` function of the `RewardsHypervisor` contract. When the `isContract` function is called with the malicious contract address, it will execute the fallback function of the malicious contract. The fallback function can then call the `deposit` or `withdraw` function of the `RewardsHypervisor` contract, which can lead to a reentrancy attack.

To prevent this vulnerability, the `isContract` function should be modified to use the `view` modifier, which will prevent it from making any state changes. Additionally, the `isContract` function should be made `public` so that it can be called from external contracts without the need for a fallback function.

#### Details

**Vulnerable Type**: Reentrancy Attack

**Vulnerable Function**: `isContract`

**Vulnerability**: The `isContract` function can be used to perform a reentrancy attack if it is called with an external contract address that has a fallback function that calls back into the `RewardsHypervisor` contract.

**Attack Scenario**: An attacker can create a malicious contract with a fallback function that calls the `isContract` function of the `RewardsHypervisor` contract. When the `isContract` function is called with the malicious contract address, it will execute the fallback function of the malicious contract. The fallback function can then call the `deposit` or `withdraw` function of the `RewardsHypervisor` contract, which can lead to a reentrancy attack.

**Mitigation**: The `isContract` function should be modified to use the `view` modifier, which will prevent it from making any state changes. Additionally, the `isContract` function should be made `public` so that it can be called from external contracts without the need for a fallback function.

### Updated Code

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
    function isContract(address _addr) public view returns (bool isContract){
				uint32 size;
				assembly {
					size := extcodesize(_addr)
				}
				return (size > 0);
		}
}
```