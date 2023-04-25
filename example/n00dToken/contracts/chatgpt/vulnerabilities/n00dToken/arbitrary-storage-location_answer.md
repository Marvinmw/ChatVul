

## Report
### Vulnerability Type: Write to Arbitrary Storage Location

The code is vulnerable to the Write to Arbitrary Storage Location attack. The `_mint` function in the `ERC777` contract writes to the `_totalSupply` and `_balances` mappings without proper authorization checks. The `_mint` function is called by the constructor of the `n00dToken` contract, which is a child contract of `ERC777`. The constructor of `n00dToken` calls `_mint` with `msg.sender` as the `account` parameter, which means that the `msg.sender` can arbitrarily increase the total supply of the token and assign the newly minted tokens to any address.

An attacker can deploy a contract that calls the constructor of `n00dToken` with their own address as one of the `defaultOperators` and a large `initialSupply`. Then, the attacker can call the `_mint` function with any address as the `account` parameter, which will increase the total supply of the token and assign the newly minted tokens to the specified address. This can be used to overwrite important variables such as the contract owner.

### Source
- https://swcregistry.io/docs/SWC-124
- https://github.com/Arachnid/uscc/tree/master/submissions-2017/doughoyte