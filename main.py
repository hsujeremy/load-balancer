DEFAULT_NUM_SERVERS = 5


class RoundRobinLoadBalancer:
    
    def __init__(self, num_servers: int = 0):
        if not num_servers:
            num_servers = DEFAULT_NUM_SERVERS
        self.servers = [i for i in range(num_servers)]
        self.counter = 0

    """
    handle_request returns the id of the server the request was routed to.
    """
    def handle_request(self) -> int:
        target = self.counter % len(self.servers)
        self.counter += 1
        return target


def main():
    print('Initializing a round robin load balancer...')
    round_robin_load_balancer = RoundRobinLoadBalancer()

    requests = 10
    print('Routing {} requests...'.format(requests))
    for i in range(requests):
        targeted_server = round_robin_load_balancer.handle_request()
        print('- R{} -> S{}'.format(i, targeted_server))


if __name__ == '__main__':
    main()