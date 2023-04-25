

### Vulnerability Report

#### Variable Shadowing

##### Description

The `owner` variable is declared twice in the `RewardsHypervisor` contract, once in the `Ownable` contract and once in the `RewardsHypervisor` contract. This can lead to confusion and unexpected behavior, as the `owner` variable in the `RewardsHypervisor` contract will shadow the `owner` variable in the `Ownable` contract, and the `onlyOwner` modifier will only check the `owner` variable in the `RewardsHypervisor` contract.

##### Recommendation

Remove the `owner` variable declaration in the `RewardsHypervisor` contract and use the `owner` variable from the `Ownable` contract instead.

##### Example

```Solidity 
contract RewardsHypervisor is Ownable {
    using SafeERC20 for IERC20;
    using SafeMath for uint256;
    IERC20 public visr;
    vVISR public vvisr;
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
    function isContract(address _addr) private returns (bool isContract){
				uint32 size;
				assembly {
					size := extcodesize(_addr)
				}
				return (size > 0);
		}
}
```