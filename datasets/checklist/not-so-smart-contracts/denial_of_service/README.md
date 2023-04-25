# Denial of Service
A malicious contract can permanently stall another contract by failing
in a strategic way. In particular, contracts that bulk perform transactions or updates using
a `for` loop can be DoS'd if a call to another contract or `transfer` fails during the loop. 


