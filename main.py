DEFAULT_NUM_SERVERS = 5


class RoundRobinLoadBalancer:
    
    def __init__(self, num_servers: int = 0):
        if not num_servers:
            num_servers = DEFAULT_NUM_SERVERS
        self.servers = [i for i in range(len(num_servers))]
        self.counter = 0

    """
    handle_request returns the id of the server the request was routed to.
    """
    def handle_request(self) -> int:
        target = self.current_server % len(self.servers)
        self.counter += 1
        return target


def main():
    print('Hello world!')


if __name__ == '__main__':
    main()