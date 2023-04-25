

## Vulnerability Type: Timestamp Dependence

The `deposit` and `withdraw` functions use the `visr` balance of the contract and the `vvisr` total supply to calculate the number of shares to mint or burn. This calculation is based on the current block timestamp, which can be manipulated by miners. A miner can post a timestamp within 15 seconds of block validation, giving them the ability to set the timestamp as a value that would increase their odds of benefitting from the function. For example, a miner can deposit VISR tokens and then modify the timestamp to a value that gives them more shares than they should receive. Similarly, a miner can burn shares and then modify the timestamp to a value that gives them more VISR tokens than they should receive.

To fix this vulnerability, the contract should not use the block timestamp to calculate the number of shares to mint or burn. Instead, it should use a block number or a block hash as a source of randomness. Alternatively, it can use an external oracle to provide a source of randomness.