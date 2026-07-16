from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from  src.exception.custom_exception import UserAlreadyExistsException,InvalidLoginException,UnauthorizedAccessException,MovieNotFoundException,BookingNotFoundException

templates = Jinja2Templates(directory="src/templates")

def user_already_exists_handler(request:Request,exc:UserAlreadyExistsException):
    return templates.TemplateResponse("error.html",{
        "request":request,"exc":exc.message
    }, status_code=409
    )

def invalid_login_handler(request:Request,exc:InvalidLoginException):
    return templates.TemplateResponse("error.html",{
        "request":request,"exc":exc.message
    },status_code=404
   )


def movie_not_found_handler(request: Request, exc: MovieNotFoundException):
    return templates.TemplateResponse(
        "error.html",{"request": request, "exc": exc.message
        },status_code=404
    )




def booking_not_found_handler(request: Request, exc: BookingNotFoundException):
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "exc": exc.message
        },
        status_code=404
    )


def unauthorized_access_handler(request: Request, exc: UnauthorizedAccessException):
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "exc": exc.message
        },
        status_code=403
    )


def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    print(exc)

    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "exc": str(exc)
        },
        status_code=500
    )


def global_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "exc": str(exc)
        },
        status_code=500
    )
