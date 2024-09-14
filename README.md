# _Release Radar_

Release Radar is a Django/React hybrid based website that allows the user see what games are releasing in respect to season
and year. The results can be narrowed down and sorted many which ways one which includes a personally impolemented hype system.

![alt text](game.png)

## Key Features

- Can be shown the current releases based on Seasons and year
- use the sort by search to sort and/or narrow the results
- Shows a multitude of different informations about said games
- Able to increase hype scores through clicking on the specific hype

## Tech

Release Radar uses a few technologies:

- [Django]
- [React]
- [PosgreSQL]
- [Psycopg2]
- [Requests]
- [Fetch]
- [Tailwindcss]
- [DjangoRestFrameWork]

## Installation

Docker (coming soon tm)
Release Radar requires a postgresql server to run
Since the .env files wont be included you need to either overwrite the database in the settings
or have your database information in your own .env
then Install the dependencies from the requirements

```sh
python -m pip install .
```

since you are starting from a new database you first have to make the migrations

```sh
python manage.py makemigrations
python manage.py migrate
```

since the api access information is also in a env you need you need your own access to the igdb api which can be obtained
at https://www.igdb.com/ for free
after you get that you can manually populate the database through the populate_database() function from the models.py
in the gameinfo folder which takes a start and a end in timestamp to choose what to pull from the api
from the gamecalenders folder

```sh
python manage.py shell
from gameinfo.models import populate_database("start_timestamp", "end_timestamp")
```

navigate to the front end folder and run npm run build

```sh
npm run build.
```

Then its finally time to go back to the gamecalender folder and run the server and then open up your local host at http://127.0.0.1:8000/

```sh
python manage.py runserver
```

## API

Release Radar uses the igdb database to pull and store game information from https://www.igdb.com/

## Development

This is just a basic project that needs a lot of work to resemble anything official I will continue to work on it in my downtime

## License

MIT
