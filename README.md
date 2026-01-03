### laod-balancer

This repository houses (soon to be) a bunch of implementations of fairly popular
load balancing algorithms, primarily as a way for me to learn about them.

Example usage:

```shellsession
$ python3 main.py
Routing 10 requests...
- R0 -> S0
- R1 -> S1
- R2 -> S2
- R3 -> S3
- R4 -> S4
- R5 -> S0
- R6 -> S1
- R7 -> S2
- R8 -> S3
```

Moving forward, I'm thinking of simulating more complex scenarios, such as
implementing some semblance of server health checks (for the more health-aware
algorithms) as well as modeling load balancing requests over time.
