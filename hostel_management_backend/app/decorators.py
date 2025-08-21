from functools import wraps
from flask_jwt_extended import get_jwt
from flask_smorest import abort

# PUBLIC_INTERFACE
def admin_required():
    """
    A decorator to protect routes that require admin privileges.
    It checks for an 'is_admin' claim in the JWT.
    If the claim is not present or not true, it aborts with a 403 error.
    This decorator must be used after @jwt_required().
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("is_admin"):
                return fn(*args, **kwargs)
            else:
                abort(403, message="Admin access required.")
        return decorator
    return wrapper
