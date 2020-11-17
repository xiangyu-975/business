from flask import g, request
from .jwt_util import verify_jwt


def jwt_authentication():
    """
    根据JWT校验用户身份
    """
    g.user_id = None
    g.is_refresh_token = False
    authentication = request.headers.get('Authentication')
    if authentication and authentication.startswith('Bearer '):
        """
        Authoriztion:Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
        eyJleHAiOjE1NzQyNzUzNjMsInVzZXJfaWQiOjExMDI0OTA1MjI4Mjk3MTc1MDUsInJlZnJlc2giOmZhbHNlfQ.
        pM27Rl61vurfptTb_lwBqKrQxivnwpQCaSiFfSxg73k
        """
        token = authentication.strip()[7:]
        payload = verify_jwt(token)
        if payload is not None:
            g.user_id = payload.get('user_id')
            g.is_refresh_token = payload.get('refresh',False)
