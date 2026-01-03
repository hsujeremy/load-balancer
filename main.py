DEFAULT_SERVER_CAPACITY = 5
DEFAULT_NUM_SERVERS = 5


class Server:

    def __init__(self, id, capacity=0):
        self.id = id
        self.load = 0
        if not capacity:
            capacity = DEFAULT_SERVER_CAPACITY
        self.capacity = capacity


class RoundRobinLoadBalancer:

    def __init__(self, num_servers: int = 0):
        if not num_servers:
            num_servers = DEFAULT_NUM_SERVERS
        self.servers = [Server(i) for i in range(num_servers)]
        self.counter = 0

    """
    handle_request returns the the server the request was routed to. If the
    target server is at capacity, handle_request returns -1.

    The fundamental limitation of static routing algorithms such as round robin
    is that they are (without modifications) blissfully unaware of actual server
    state. In this case, this means that the request will be routed to the
    "next" server regardless of whether the server is overloaded or not.
    """
    def handle_request(self) -> Server:
        target = self.counter % len(self.servers)
        self.counter += 1
        self.servers[target].load += 1
        return self.servers[target]


def main():
    print('Initializing a round robin load balancer...')
    round_robin_load_balancer = RoundRobinLoadBalancer()

    requests = 10
    print('Routing {} requests...'.format(requests))
    for i in range(requests):
        targeted_server = round_robin_load_balancer.handle_request()
        print('- R{} -> S{} (Load: {} Capacity: {})'.format(
            i,
            targeted_server.id,
            targeted_server.load,
            targeted_server.capacity,
        ))


if __name__ == '__main__':
    main()