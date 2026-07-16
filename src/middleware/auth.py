from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses  import RedirectResponse

class Auth(BaseHTTPMiddleware):
    async def dispatch(self,request:Request,call_next):
        public_urls = ["/","/login","/register"]

        if request.url.path in public_urls:
            return await call_next(request)


        if request.session.get("user_id"):
            return await call_next(request)


        return RedirectResponse(url="/login",status_code=302)

    