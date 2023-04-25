## Transaction-Ordering Dependence

Transactions on Ethereum are grouped together in blocks which are processed on a semi-regular interval, ~15 seconds. Before transactions are placed in blocks, they are broadcasted to the mempool where block builders can then proceed to place them as is economically optimal. What's important to understand here is that the mempool is public and thus anyone can see transactions before they're executed, giving them the power to front-run by placing their own transaction executing the same, or a similar, action with a higher gas price. Frontrunning has become so prevalent as a result of generalized frontrunning bots becoming more and more common, which work by observing the mempool for profitable, replicable transactions which they can replace for their own benefit. [Ethereum is a Dark Forest](https://www.paradigm.xyz/2020/08/ethereum-is-a-dark-forest).

One solution to transaction-ordering dependence is to use a commit-reveal scheme in the case of information being submitted on-chain. This works by having the submittor send in a hash of the information, storing that on-chain along with the user address so that they may later reveal the answer along with the salt to prove that they were indeed correct. Another solution is to simply use a private mempool such as [Flashbots](https://www.flashbots.net/).

### Sources

- https://consensys.github.io/smart-contract-best-practices/known_attacks/#front-running-aka-transaction-ordering-dependence
- https://users.encs.concordia.ca/~clark/papers/2019_wtsc_front.pdf
- https://swcregistry.io/docs/SWC-114