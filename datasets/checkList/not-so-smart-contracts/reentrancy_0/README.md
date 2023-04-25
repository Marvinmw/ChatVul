# Re-entrancy
A state variable is changed after a contract uses `call.value`. The attacker uses
[a fallback function](ReentrancyExploit.sol#L26-L33)—which is automatically executed after
Ether is transferred from the targeted contract—to execute the vulnerable function again, *before* the
state variable is changed.
