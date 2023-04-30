class FirehoseExponentialBackoff:

    def __init__(self, initial_wait: int = 0, base: int = 2, max_wait: int = 60):
        self._initial_wait = initial_wait
        self._base = base
        self._max_wait = max_wait
        self._failures = 0

    def reset(self):
        self._failures = 0

    def next_sleep_time(self) -> int:
        sleep_time = self._initial_wait

        if self._failures > 0:
            sleep_time = min(self._max_wait, self._base ** self._failures)
        
        self._failures += 1

        return sleep_time
            