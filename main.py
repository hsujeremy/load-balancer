import random


DEFAULT_SERVER_CAPACITY = 2
DEFAULT_NUM_SERVERS = 3


class Server:

    def __init__(self, id, capacity=0):
        self.id = id
        self.load = 0
        if not capacity:
            capacity = DEFAULT_SERVER_CAPACITY
        self.capacity = capacity


class RoundRobinLoadBalancer:
    """
    Implements a round robin load balancer. Round robin load balancing is the
    simplest variant of static load balancing: given a set of servers, it cycles
    over each one one request at a time.

    Pros:
    - Extremely simple to implement and reason about
    - Distributes requests evenly across all servers
    - Statelessness implementation

    Cons:
    - Doesn't consider servers with different capacities, processing power, etc.
    - Doesn't consider the current server state (e.g., health)
    - Doesn't support sticky connections (due to its statelessness)
    - Risks convoy effects where multiple expensive requests are forwarded to
      multiple servers, causing bottlenecks on all of them
    """

    def __init__(self, num_servers: int = 0):
        if not num_servers:
            num_servers = DEFAULT_NUM_SERVERS
        self.servers = [Server(i) for i in range(num_servers)]
        self.counter = 0

    """
    The fundamental limitation of static routing algorithms such as round robin
    is that they are (without modifications) blissfully unaware of actual server
    state. In this case, this means that the request will be routed to the
    "next" server regardless of whether the server is overloaded or not.
    """
    def forward_request(self) -> Server:
        target = self.counter % len(self.servers)
        self.counter += 1
        self.servers[target].load += 1
        return self.servers[target]


class WeightedRoundRobinLoadBalancer:
    """
    Implements a weighted round robin load balancer. Weight round robin load
    balancing assigns weights to each server and prioritizes servers with higher
    weights. These weights can include properties such as CPU processing power.

    Weight round robin load balancing presents an improvement over simple round
    robin forwarding in that it factors in heterogeneity in server configuration
    during routing. However, it is also stateless (which has both pros and cons)
    and faces the same drawback of any static load balancing algorithm, which is
    that it doesn't consider the live state of a server.
    """

    def __init__(self, num_servers: int = 0):
        if not num_servers:
            num_servers = DEFAULT_NUM_SERVERS
        self.servers = [
            Server(i, capacity=random.randint(1, 5))
            for i in range(num_servers)
        ]
        self.counter = 0
        # Note also that we're maintaining internal state on a server's capacity
        # instead of considering the server's actual load. This is because this
        # algorithm is still static.
        self.seen_count_for_server = [0 for _ in range(num_servers)]

    """
    TODO: The current implementation is naive as it forwards all requests to a
    single server before it runs out of "space." We should implement the
    interleaved approach in order to smooth out request forwarding amongst
    servers over time.
    """
    def forward_request(self) -> Server:
        target = -1
        while True:
            target = self.counter % len(self.servers)
            if self.seen_count_for_server[target] < self.servers[target].capacity:
                break
            self.seen_count_for_server[target] = 0
            self.counter += 1

        # Should never fail as target must be set before breaking from the loop.
        assert target != -1

        self.seen_count_for_server[target] += 1
        self.servers[target].load += 1
        return self.servers[target]


def main():
    print('Initializing a round robin load balancer...')
    round_robin_load_balancer = RoundRobinLoadBalancer()
    requests = 10
    print('Routing {} requests...'.format(requests))
    for i in range(requests):
        targeted_server = round_robin_load_balancer.forward_request()
        print('- R{} -> S{} (Load: {} Capacity: {})'.format(
            i,
            targeted_server.id,
            targeted_server.load,
            targeted_server.capacity,
        ))

    print('Initializing a weighted round robin load balancer...')
    weighted_round_robin_load_balancer = WeightedRoundRobinLoadBalancer()
    requests = 10
    print('Routing {} requests...'.format(requests))
    for i in range(requests):
        targeted_server = weighted_round_robin_load_balancer.forward_request()
        print('- R{} -> S{} (Load: {} Capacity: {})'.format(
            i,
            targeted_server.id,
            targeted_server.load,
            targeted_server.capacity,
        ))


if __name__ == '__main__':
    main()
