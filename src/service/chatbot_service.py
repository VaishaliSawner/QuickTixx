import os

from openai import AsyncOpenAI
from dotenv import load_dotenv

from src.service.movie_service import MovieService

load_dotenv()


client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


class ChatbotService:
    def __init__(self, session):
        self.movie_service = MovieService(session)

    async def get_reply(self, user_message: str, history: list[dict]) -> str:

        movies = await self.movie_service.get_all_movies()

        if movies:
            movie_list = "\n".join(
                f"- {m.movie_name} ({m.language}, {m.genre}) - Rs.{m.price}, "
                f"{m.available_seats} seats left"
                for m in movies
            )
        else:
            movie_list = "No movies are currently available."

        system_prompt = (
            "You are a friendly assistant for QuickTix, a movie ticket booking "
            "website. Help users find movies, answer questions about genres, "
            "languages, prices and how to book tickets. Only recommend movies "
            "from the list below, do not make up movies. Keep answers short "
            "and conversational.\n\n"
            f"Available movies:\n{movie_list}"
        )

        messages = (
            [{"role": "system", "content": system_prompt}]
            + history
            + [{"role": "user", "content": user_message}]
        )

        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=500,
            messages=messages,
        )

        return response.choices[0].message.content