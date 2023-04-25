

## Report

### Vulnerability Type
Transaction-Ordering Dependence

### Vulnerability Description
The `deposit` function of the `RewardsHypervisor` contract is vulnerable to transaction-ordering dependence. The function accepts a `visrDeposit` parameter, which is the amount of `visr` tokens to be deposited. The function calculates the number of `vvisr` tokens to be minted based on the current total supply of `vvisr` tokens and the balance of `visr` tokens held by the contract. An attacker can front-run a transaction by submitting a transaction with a higher gas price that deposits a larger amount of `visr` tokens before the victim's transaction is executed. This would result in the attacker receiving a larger number of `vvisr` tokens than the victim, even if the victim's transaction was submitted first.

### Recommendation
One solution to transaction-ordering dependence is to use a commit-reveal scheme in the case of information being submitted on-chain. This works by having the submittor send in a hash of the information, storing that on-chain along with the user address so that they may later reveal the answer along with the salt to prove that they were indeed correct. Another solution is to simply use a private mempool such as Flashbots.

In this case, the contract can be updated to use a commit-reveal scheme to prevent front-running attacks. The `deposit` function can be split into two separate functions: `commit` and `deposit`. The `commit` function accepts a hash of the `visrDeposit` parameter and stores it on-chain along with the user address. The `deposit` function can be called after a certain amount of time has passed, during which the user can reveal the actual `visrDeposit` value along with a salt to prove that they were indeed correct. This would prevent front-running attacks as the actual `visrDeposit` value would not be known until after the commit phase has ended.

Another solution is to use a private mempool such as Flashbots. Flashbots allows miners to bundle transactions and execute them off-chain, preventing front-running attacks.

### Example
Here's an example of how the `deposit` function can be split into two separate functions:

```
function commit(
    bytes32 hash,
    address payable from,
    address to
) external {
    require(to != address(0) && to != address(this), "to");
    require(from != address(0) && from != address(this), "from");
    // Store the hash on-chain along with the user address
    // ...
}

function deposit(
    uint256 visrDeposit,
    bytes32 salt,
    address payable from,
    address to
) external returns (uint256 shares) {
    require(visrDeposit > 0, "deposits must be nonzero");
    require(to != address(0) && to != address(this), "to");
    require(from != address(0) && from != address(this), "from");
    // Verify that the hash of the visrDeposit and salt matches the stored hash
    // ...
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

In this example, the `commit` function accepts a hash of the `visrDeposit` parameter and stores it on-chain along with the user address. The `deposit` function accepts the actual `visrDeposit` value, a salt, and the user and recipient addresses. The function verifies that the hash of the `visrDeposit` and salt matches the stored hash before proceeding with the deposit. This ensures that the actual `visrDeposit` value is not known until after the commit phase has ended, preventing front-running attacks.