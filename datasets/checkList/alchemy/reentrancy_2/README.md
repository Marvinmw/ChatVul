Reentrancy is a programming method where an external function call causes the execution of a function to pause. Conditions in the logic of the external function call allow it to call itself repeatedly before the original function execution is finished.
A reentrancy attack takes advantage of unprotected external calls and can be a particularly damaging exploit, draining all of the funds in your contract if not handled properly.
A reentrancy guard is a modifier that causes execution to fail whenever a reenterancy act is discovered. This also prevents more than one function from being executed at a time by locking the contract.

