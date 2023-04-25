# Bad Randomness
Pseudorandom number generation on the blockchain is generally unsafe. There are a number of reasons for this, including:

- The blockchain does not provide any cryptographically secure source of randomness. 

- Everything in a contract is publicly visible. Random numbers cannot be generated or stored in the contract until after all lottery entries have been stored.

- Computers will always be faster than the blockchain. Any number that the contract could generate can potentially be precalculated off-chain before the end of the block.


