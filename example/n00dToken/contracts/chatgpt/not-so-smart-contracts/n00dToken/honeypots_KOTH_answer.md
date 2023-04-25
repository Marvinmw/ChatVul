

## Vulnerability Report

### Variable Shadowing

#### Vulnerability Type
Variable Shadowing

#### Vulnerable Code
```Solidity 
contract n00dToken is ERC777 {
    constructor(uint256 initialSupply, address[] memory defaultOperators)
        ERC777("n00dle", "n00d", defaultOperators)
    {
        _mint(msg.sender, initialSupply, "", "");
    }
}
```

#### Description
The `n00dToken` contract inherits from the `ERC777` contract and has a constructor that calls the `_mint` function to mint tokens and assign them to the contract deployer. However, the `n00dToken` contract defines a `constructor` that has the same name as the `ERC777` contract's `constructor`. This results in the `ERC777` contract's `constructor` being shadowed and not being called when the `n00dToken` contract is deployed. As a result, the `_ERC1820_REGISTRY` is not initialized, which could lead to unexpected behavior.

#### Recommendation
Rename the `n00dToken` contract's constructor to a different name to avoid shadowing the `ERC777` contract's constructor.

#### Example
```Solidity 
contract n00dToken is ERC777 {
    constructor(uint256 initialSupply, address[] memory defaultOperators)
        ERC777("n00dle", "n00d", defaultOperators)
    {
        _mint(msg.sender, initialSupply, "", "");
    }
}
```