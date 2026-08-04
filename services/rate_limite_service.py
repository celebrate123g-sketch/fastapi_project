import time


class RateLimiter:

    def __init__(

        self,

        requests: int,

        window: int

    ):

        self.requests = requests

        self.window = window

        self.storage = {}

    def check(

        self,

        client: str

    ):

        now = time.time()

        if client not in self.storage:

            self.storage[client] = []

        requests = self.storage[client]

        requests[:] = [

            request

            for request in requests

            if now - request < self.window

        ]

        if len(requests) >= self.requests:

            return False, self.window

        requests.append(now)

        remaining = self.requests - len(requests)

        reset = int(

            self.window - (now - requests[0])

        )

        return True, {

            "remaining": remaining,

            "reset": reset

        }