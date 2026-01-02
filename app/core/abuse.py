import time

BLOCKED = {}


def block(ip: str, seconds: int = 60):
    BLOCKED[ip] = time.time() + seconds


def is_blocked(ip: str) -> bool:
    until = BLOCKED.get(ip)
    if not until:
        return False
    if time.time() > until:
        del BLOCKED[ip]
        return False
    return True
