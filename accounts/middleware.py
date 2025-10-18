# accounts/middleware.py
import time
from django.contrib.auth import logout

IDLE_TIMEOUT = 300  # seconds (5 minutes)

class IdleSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = time.time()
            last = request.session.get("last_activity", now)
            if now - float(last) > IDLE_TIMEOUT:
                logout(request)
                # session is cleared; subsequent access will hit LOGIN_URL
            request.session["last_activity"] = now
        return self.get_response(request)
