# Unchecked External Call

Certain Solidity operations known as "external calls", require the developer to manually ensure that the operation succeeded. This is in contrast to operations which throw an exception on failure. If an external call fails, but is not checked, the contract will continue execution as if the call succeeded. This will likely result in buggy and potentially exploitable behavior from the contract.
