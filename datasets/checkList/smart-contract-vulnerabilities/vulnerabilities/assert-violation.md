## Assert Violation

In Solidity `0.4.10`, the following functions were created: `assert()`, `require()`, and `revert()`. Here we'll discuss the assert function and how to use it.

Formally said, the `assert()` funtion is meant to assert invariants; informally said, `assert()` is an overly assertive bodyguard that protects your contract, but steals your gas in the process. Properly functioning contracts should never reach a failing assert statement. If you've reached a failing assert statement, you've either improperly used `assert()`, or there is a bug in your contract that puts it in an invalid state.

If the condition checked in the `assert()` is not actually an invariant, it's suggested that you replace it with a `require()` statement.

### Sources

- https://swcregistry.io/docs/SWC-110
- https://media.consensys.net/when-to-use-revert-assert-and-require-in-solidity-61fb2c0e5a57