

Vulnerability Type: Incorrect Function Name

In the `RewardsHypervisor` contract, the constructor function is named `constructor` instead of the name of the contract. This can cause issues with the deployment of the contract and make it harder to read and understand the code. It is recommended to use the name of the contract as the constructor function name.

To fix this issue, the constructor function should be renamed to `RewardsHypervisor`:

```Solidity
constructor(
    address _visr,
    address _vvisr
) {
    visr = IERC20(_visr);
    vvisr = vVISR(_vvisr);
    owner = msg.sender;
}
```