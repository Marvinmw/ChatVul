

## Vulnerability Report

### Description

The code is vulnerable to delegatecall to untrusted callee attack. 

### Vulnerability Type

Delegatecall to Untrusted Callee

### Vulnerable Code

```Solidity
function _callTokensToSend(
        address operator,
        address from,
        address to,
        uint256 amount,
        bytes memory userData,
        bytes memory operatorData
    ) private {
        address implementer = _ERC1820_REGISTRY.getInterfaceImplementer(from, _TOKENS_SENDER_INTERFACE_HASH);
        if (implementer != address(0)) {
            IERC777Sender(implementer).tokensToSend(operator, from, to, amount, userData, operatorData);
        }
    }
```

### Details

The `_callTokensToSend` function uses `delegatecall` to call the `tokensToSend` function of the contract at the address returned by `_ERC1820_REGISTRY.getInterfaceImplementer`. This means that an attacker could register a malicious contract as the implementer of the `ERC777TokensSender` interface, and then use this to execute arbitrary code in the context of the `n00dToken` contract.

### Example

An attacker could deploy a contract with the following code:

```Solidity
contract MaliciousContract {
    function tokensToSend(
        address operator,
        address from,
        address to,
        uint256 amount,
        bytes memory userData,
        bytes memory operatorData
    ) public {
        // Malicious code here
    }
}
```

They could then register this contract as the implementer of the `ERC777TokensSender` interface using the `_ERC1820_REGISTRY.setInterfaceImplementer` function. Finally, they could call the `send` function of the `n00dToken` contract, which would call the `tokensToSend` function of the attacker's contract using `delegatecall`, allowing the attacker to execute their malicious code in the context of the `n00dToken` contract.

### Recommendation

To fix this vulnerability, the `_callTokensToSend` function should use `call` instead of `delegatecall`. This will ensure that the called contract is executed in its own context, rather than in the context of the calling contract.

### References

- https://swcregistry.io/docs/SWC-112
- https://solidity.readthedocs.io/en/latest/introduction-to-smart-contracts.html#delegatecall-callcode-and-libraries
- https://blog.sigmaprime.io/solidity-security.html#delegatecall
- https://ethereum.stackexchange.com/questions/3667/difference-between-call-callcode-and-delegatecall