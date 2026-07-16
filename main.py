import os
import uuid
import shutil
from fastapi import FastAPI,Request,Form,UploadFile,File
from starlette.responses import RedirectResponse

from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from src.service.chatbot_service import ChatbotService
from src. model.movie  import Movie
from src.model.booking import Booking
from src.service.booking_service import BookingService
from src.model.user import User
from src.service.user_service import UserService
from src.service.movie_service import MovieService

from src.db_config.database import SessionLocal
from src.middleware.auth import Auth
from src.exception.custom_exception import UserAlreadyExistsException,InvalidLoginException,MovieNotFoundException,BookingNotFoundException,UnauthorizedAccessException

from sqlalchemy.exc import SQLAlchemyError
from src.exception.exception_handler import user_already_exists_handler,invalid_login_handler,movie_not_found_handler,booking_not_found_handler,unauthorized_access_handler,sqlalchemy_exception_handler, global_exception_handler
app =FastAPI()
app.mount("/static",StaticFiles(directory="src/static"),name="static")
app.add_middleware(Auth)
app.add_middleware(SessionMiddleware,secret_key="movie_ticket_secret")

#app.add_middleware(Auth)

templates = Jinja2Templates(directory="src/templates")

UPLOAD_DIR = "src/static/images"

def save_uploaded_image(image: UploadFile) -> str:
    ext = os.path.splitext(image.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return f"/static/images/{filename}"

app.add_exception_handler(UserAlreadyExistsException, user_already_exists_handler)
app.add_exception_handler(InvalidLoginException, invalid_login_handler)
app.add_exception_handler(MovieNotFoundException, movie_not_found_handler)
app.add_exception_handler(BookingNotFoundException, booking_not_found_handler)
app.add_exception_handler(UnauthorizedAccessException, unauthorized_access_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)


@app.get("/")
async def home(request:Request):
    return templates.TemplateResponse(request,"home.html",{"request":request})

@app.get("/register")
async def register(request:Request):
    return templates.TemplateResponse(request,"register.html",{"request":request})

@app.post("/register")
async def register(request:Request,
                   name:str=Form(...),
                   email:str=Form(...),
                   password:str=Form(...)):
    async with SessionLocal.begin() as session:
        user=User(
            name=name,
            email=email,
            password=password
        )
        user_service=UserService(session)
        await user_service.register_user(user)
        return RedirectResponse("/login",status_code=303)

@app.get("/login")
async def login(request:Request):
    return templates.TemplateResponse(request,"login.html",{"request":request})

@app.post("/login")
async def login(request:Request,
                email:str=Form(...),
                password:str=Form(...)
                ):
    async with SessionLocal.begin() as session:
        user_service=UserService(session)
        user=await user_service.login_user(email,password)

        request.session["user_id"] = user.id
        request.session["role"] = user.role
        return RedirectResponse("/dashboard",status_code=303)


@app.get("/logout")
async def logout(request:Request):
    request.session.clear()
    return RedirectResponse("/login",status_code=303)

@app.get("/dashboard")
async def dashboard(request:Request):
    async with SessionLocal() as session:
        movie_service=MovieService(session)
        movies=await movie_service.get_all_movies()
        return templates.TemplateResponse(request,"dashboard.html",{"request":request,
                                                "movies":movies,
                                                 "total_movies":len(movies),
                                                 "role":request.session.get("role"),
                                                 "user_id":request.session.get("user_id")})

@app.get("/movies")
async def movies(request:Request,message:str | None = None):
    async with SessionLocal() as session:
        movie_service=MovieService(session)
        movies=await movie_service.get_all_movies()
        return templates.TemplateResponse(request,"movies.html",{
            "request":request,
            "movies":movies,
            "message":message
        })

@app.get("/movie/{id}")
async def movie_details(request:Request,id:int):
    async with SessionLocal() as session:
        movie_service=MovieService(session)
        movie = await movie_service.get_movie_by_id(id)
        return templates.TemplateResponse(request,"movie_details.html",{"request":request,"movie":movie})

@app.get("/add-movie")
async def add_movie(request:Request):
    if request.session.get("role") !="admin":
        raise UnauthorizedAccessException()

    return templates.TemplateResponse(request,"add_movie.html",{"request":request})

@app.post("/add-movie")
async def add_movie(request:Request,
                    movie_name:str=Form(...),
                    language:str=Form(...),
                    genre:str=Form(...),
                    duration:str=Form(...),
                    price:float=Form(...),
                    available_seats:int=Form(...),
                    description:str=Form(...),
                    image:UploadFile=File(...)):
    if request.session.get("role") !="admin":
        raise UnauthorizedAccessException()

    image_path = save_uploaded_image(image)

    async with SessionLocal.begin() as session:
        movie=Movie(
            movie_name=movie_name,
            language=language,
            genre=genre,
            duration=duration,
            price=price,
            available_seats=available_seats,
            description=description,
            image=image_path
        )
        movie_service=MovieService(session)
        await movie_service.create_movie(movie)

        return RedirectResponse("/movies?message=Movie Added Successfully",status_code=303)

@app.get("/edit-movie/{id}")
async def edit_movie(request: Request,id: int):

    if request.session.get("role") != "admin":
        raise UnauthorizedAccessException()

    async with SessionLocal() as session:
        movie_service = MovieService(session)
        movie = await movie_service.get_movie_by_id(id)
        return templates.TemplateResponse( request, "edit_movie.html",  {"request": request,"movie": movie})


@app.post("/edit-movie/{id}")
async def edit_movie(
    request: Request,
    id: int,
    movie_name: str = Form(...),
    language: str = Form(...),
    genre: str = Form(...),
    duration: str = Form(...),
    price: float = Form(...),
    available_seats: int = Form(...),
    description: str = Form(...),
    image: UploadFile | None = File(None)
):

    if request.session.get("role") != "admin":
        raise UnauthorizedAccessException()
    async with SessionLocal.begin() as session:
        movie_service = MovieService(session)
        db_movie = await movie_service.get_movie_by_id(id)

        image_path = db_movie.image
        if image and image.filename:
            image_path = save_uploaded_image(image)

        movie = Movie(
            id=id,
            movie_name=movie_name,
            language=language,
            genre=genre,
            duration=duration,
            price=price,
            available_seats=available_seats,
            description=description,
            image=image_path
        )

        await movie_service.update_movie(movie, db_movie)
        return RedirectResponse("/movies?message=Movie Updated Successfully",status_code=303)


@app.get("/delete-movie/{id}")
async def delete_movie(request: Request,id: int):

    if request.session.get("role") != "admin":
        raise UnauthorizedAccessException()
    async with SessionLocal.begin() as session:
        movie_service = MovieService(session)
        await movie_service.delete_movie(id)
        return RedirectResponse( "/movies?message=Movie Deleted Successfully",status_code=303)

@app.get("/book-ticket/{movie_id}")
async def book_ticket(request: Request,movie_id: int):
    async with SessionLocal() as session:
        movie_service = MovieService(session)
        movie = await movie_service.get_movie_by_id(movie_id)
        return templates.TemplateResponse(request,"book_ticket.html", {"request": request,"movie": movie })


@app.post("/book-ticket")
async def book_ticket(request:Request,movie_id:int=Form(...),quantity:int=Form(...)):
    async with SessionLocal.begin() as session:
        booking=Booking(
            user_id=request.session.get("user_id"),
            movie_id=movie_id,
            quantity=quantity
        )
        booking_service=BookingService(session)
        await booking_service.book_ticket(booking)
        return RedirectResponse("/my-bookings?message=Ticket Booked Successfully",status_code=303)


@app.get("/my-bookings")
async def my_bookings(request: Request,message: str | None = None):

    async with SessionLocal() as session:
        booking_service = BookingService(session)
        bookings = await booking_service.get_my_bookings(
            request.session.get("user_id")
        )
        return templates.TemplateResponse(request, "my_bookings.html",  {"request": request,"bookings": bookings,"message": message})

@app.get("/cancel-booking/{id}")
async def cancel_booking(request: Request,id: int):
    async with SessionLocal.begin() as session:
        booking_service = BookingService(session)
        await booking_service.cancel_booking(id)
        return RedirectResponse( "/my-bookings?message=Booking Cancelled Successfully",status_code=303)




@app.get("/chatbot")
async def chatbot_page(request: Request):
    return templates.TemplateResponse(request, "chatbot.html", {"request": request})


@app.post("/chatbot/ask")
async def chatbot_ask(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    history = data.get("history", [])

    async with SessionLocal() as session:
        chatbot_service = ChatbotService(session)
        reply = await chatbot_service.get_reply(user_message, history)
        return {"reply": reply}



