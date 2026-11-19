from fastapi import FastAPI

app = FastAPI()

games = [
    {"id": 1, "title": "Pokemon Platinum Version", "genres": ["RPG"], "release_year": 2008},
    {"id": 2, "title": "The Witcher 3: Wild Hunt", "genres": ["RPG", "Action Adventure"], "release_year": 2015},
    {"id": 3, "title": "Red Dead Redemption 2", "genres": ["Western", "Action Adventure"], "release_year": 2018}
]


@app.get("/games")
def get_games():
    return games
