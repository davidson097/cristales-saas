def require_role(role: str):
    def _inner():
        return True
    return _inner
