## Report

### Vulnerability Type
Shadowing State Variables

### Vulnerability Details
The `RewardsHypervisor` contract has two state variables named `visr` and `vvisr`. These variables are also used as function parameters and local variables in the `deposit` and `withdraw` functions. This can lead to unintended side effects and make the code difficult to read and maintain. 

For example, in the `deposit` function, the `visr` variable is used to refer to both the state variable and the function parameter. This can cause confusion and make it difficult to understand which variable is being used in a particular context. Similarly, in the `withdraw` function, the `vvisr` variable is used to refer to both the state variable and the local variable. 

### Recommendation
To avoid this vulnerability, it is recommended to use unique names for state variables, function parameters, and local variables. This will make the code easier to read and maintain, and reduce the risk of unintended side effects. 

In this case, the state variables `visr` and `vvisr` should be renamed to avoid shadowing. For example, they could be renamed to `_visr` and `_vvisr`. Similarly, the function parameters and local variables should also be given unique names. 

### Reference
- https://swcregistry.io/docs/SWC-119