In Solidity, tx.origin is a global variable that returns the address of the account that sent the transaction. Using the tx.origin variable for authorization may expose a contract to compromise if an authorized account calls into a malicious contract.
Avoiding the use of tx.origin for authentication purposes is the best method to guard against tx.origin attacks instead use msg.sender in its place.
The difference between tx.origin and msg.sender is msg.sender, the owner, can be a contract while tx.origin the owner can never be a contract.
