# Game Tracker Project Plan

## What can a user do?

### If visitor (not logged in)

- Search for games
- See a game's details
- Create an account and log in

### If registered user (logged in)

- Add a game to my list with a status: Playing, Completed, On hold, Dropped, Plan to play
- Give a game a score from 1 to 10 and write notes
- Edit or remove a list entry
- See my list, filter it by status and sort it by score or title
- See my stats: games per status, average score, top genres

### Leaving out for now

- Social, public profiles, friends, etc

## Pages

| Page        | URL        | Shows                                                                                | Actions                                           | Login needed   |
| ----------- | ---------- | ------------------------------------------------------------------------------------ | ------------------------------------------------- | -------------- |
| Search      | /          | Search box and results (cover, title, year)                                          | Open a game                                       | No             |
| Game detail | /games/:id | Cover, title, release year, genres, developer, publisher, and my entry if I have one | Add to list, edit status, score and notes, remove | To add or edit |
| My list     | /my-list   | My entries: title, status, score                                                     | Filter by status, sort, open a game               | Yes            |
| Stats       | /stats     | Games per status, average score, top genres                                          | None                                              | Yes            |
| Log in      | /login     | Email and password form                                                              | Log in                                            | No             |
| Register    | /register  | Email and password form                                                              | Create an account                                 | No             |

## Data

### users

| Column        | Type     | Rules             |
| ------------- | -------- | ----------------- |
| id            | integer  | primary key       |
| email         | text     | required, unique  |
| password_hash | text     | required          |
| created_at    | datetime | set automatically |

### games

| Column       | Type    | Rules                                         |
| ------------ | ------- | --------------------------------------------- |
| id           | integer | primary key                                   |
| rawg_id      | integer | unique, empty only for seed games             |
| title        | text    | required                                      |
| release_year | integer | optional                                      |
| cover_url    | text    | optional                                      |
| developers   | text    | optional, display only, e.g. "CD Projekt Red" |
| publishers   | text    | optional, display only                        |

### genres

| Column | Type    | Rules            |
| ------ | ------- | ---------------- |
| id     | integer | primary key      |
| name   | text    | required, unique |

### game_genres

| Column   | Type    | Rules                 |
| -------- | ------- | --------------------- |
| game_id  | integer | foreign key to games  |
| genre_id | integer | foreign key to genres |

### list_entries

| Column                 | Type     | Rules                                                |
| ---------------------- | -------- | ---------------------------------------------------- |
| id                     | integer  | primary key                                          |
| user_id                | integer  | foreign key to users                                 |
| game_id                | integer  | foreign key to games                                 |
| status                 | text     | playing, completed, on_hold, dropped or plan_to_play |
| score                  | integer  | optional, 1 to 10                                    |
| notes                  | text     | optional                                             |
| created_at, updated_at | datetime | set automatically                                    |

A user can add each game only once.

## API endpoints

| Method | Path                 | Login | Purpose                                                        | Success    |
| ------ | -------------------- | ----- | -------------------------------------------------------------- | ---------- |
| POST   | /api/auth/register   | No    | Create an account                                              | 201        |
| POST   | /api/auth/login      | No    | Log in and get a token                                         | 200        |
| GET    | /api/me              | Yes   | Get the logged-in user                                         | 200        |
| GET    | /api/games           | No    | List catalog games, with search, filters and pages             | 200        |
| GET    | /api/games/{id}      | No    | Get one game                                                   | 200        |
| GET    | /api/rawg/search?q=  | No    | Search RAWG without saving anything                            | 200        |
| POST   | /api/games/import    | No    | Save a RAWG game to the catalog, or return it if already saved | 201 or 200 |
| GET    | /api/me/entries      | Yes   | My list, with status filter, sorting and pages                 | 200        |
| POST   | /api/me/entries      | Yes   | Add a game to my list                                          | 201        |
| PATCH  | /api/me/entries/{id} | Yes   | Change status, score or notes                                  | 200        |
| DELETE | /api/me/entries/{id} | Yes   | Remove from my list                                            | 204        |
| GET    | /api/me/stats        | Yes   | My stats                                                       | 200        |

Common errors: 401 not logged in, 404 not found, 409 game already in my list, 422 invalid data.

## How games get into the catalog

1. Search asks RAWG through our backend. Nothing is saved.
2. Opening a result imports the game into our database, or reuses it if it's already there.
3. Pages, list entries and stats always use our own copy.
