

Vulnerability Type: Reentrancy Attack

In the `withdraw` function, the `from` address is used to call the `IVisor(from).owner()` function. This can be a potential vulnerability as the `from` address can be a malicious contract that can execute a reentrancy attack by calling back the `withdraw` function before it completes its execution. This can result in the attacker being able to withdraw more tokens than they are entitled to.

To mitigate this vulnerability, it is recommended to use the `nonReentrant` modifier from the OpenZeppelin library to prevent reentrancy attacks.