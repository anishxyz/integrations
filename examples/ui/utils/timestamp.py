from time import time


def unix_ts() -> int:
    return int(time())
