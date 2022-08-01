# Django Youtube Scrapper

## About

This is a demo project for Scrapping Youtube channel.

It was made using **Python 3.8** + **Django 4** and database is **MySQL**.

## Prerequisites

\[Optional\] Install virtual environment:

```bash
$ python -m virtualenv env
```

\[Optional\] Activate virtual environment:

On macOS and Linux:
```bash
$ source env/bin/activate
```

On Windows:
```bash
$ .\env\Scripts\activate
```

Install dependencies:
```bash
$ pip install -r requirements.txt
```

## How to run

Create `.env` file into root directory or the project and set variables with appropriate value.

### Default

You can run the application from the command line with manage.py.
Go to the root folder of the application.

Run migrations:
```bash
$ python manage.py migrate
```

Scrap channel data:
```bash
$ python manage.py channel_scrapper
```

Run server on port 8000:
```bash
$ python manage.py runserver 8000
```

Go to the web browser and visit `http://localhost:8000/api/videos`

Filter by tag name:

`http://localhost:8000/api/videos?tags=python`

### Tests

#### Default
Activate virtual environment:

On macOS and Linux:
```bash
$ source env/bin/activate
```

On Windows:
```bash
$ .\env\Scripts\activate
```

Running tests:
```bash
$ python manage.py test utube
```