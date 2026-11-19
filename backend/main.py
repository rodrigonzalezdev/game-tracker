from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Game(BaseModel):
    id: int
    rawg_id: int | None = None
    title: str
    release_year: int | None = None
    cover_url: str | None = None
    developers: str | None = None
    publishers: str | None = None
    genres: list[str] = []


app = FastAPI()

games = [
    Game(id=1, title="Pokemon Platinum Version", genres=["RPG"], release_year=2008),
    Game(
        id=2,
        title="The Witcher 3: Wild Hunt",
        release_year=2015,
        developers="CD Projekt Red",
        publishers="CD Project Red",
        genres=["RPG", "Action Adventure"],
    ),
]


@app.get("/api/games")
def get_games() -> list[Game]:
    return games


@app.get("/api/games/{game_id}")
def get_game(game_id: int) -> Game:
    for game in games:
        if game.id == game_id:
            return game

    raise HTTPException(status_code=404, detail="Game not found")
