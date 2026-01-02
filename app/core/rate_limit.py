from slowapi import Limiter
from slowapi.util import get_remote_address


def user_key(request):
    # During tests we set a unique client id header so rate-limit counters
    # don't leak between tests. Prefer that header when present.
    test_client_id = request.headers.get("X-Test-Client-ID")
    if test_client_id:
        return test_client_id

    user = getattr(request.state, "user", None)
    if user:
        return str(user.pk)
    return get_remote_address(request)


def workspace_key(request):
    # Prefer explicit workspace header, fall back to test client id for tests,
    # and finally to the remote address.
    workspace = request.headers.get("X-Workspace")
    if workspace:
        return workspace

    test_client_id = request.headers.get("X-Test-Client-ID")
    if test_client_id:
        return test_client_id

    return get_remote_address(request)


limiter = Limiter(key_func=user_key)
