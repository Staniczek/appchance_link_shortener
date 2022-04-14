# Link shortener

## Launching the application
To run the application, you will need docker and docker-compose installed.
1. Build your containers and install its dependencies.
``` docker-compose build ```
2. Start your services and run it.
``` docker-compose up -d ```
3. Do the migration.
``` docker-compose run web python manage.py migrate ```
4. Restart django container.
``` docker-compose restart web ```

## Change the length of shortened links
To change the length of shortened links, change the value of the SHORTENED_LINK_LENGTH variable in the appchance/settings.py file

## API endpoints
The following endpoints api allow you to create a shortened link, read information about the link and redirect to the page.

### GET /
Returns a list of all shortened links.
#### Response
```json
    [
        {
            "shortened_link": "http://127.0.0.1:8000/TZjUn",
            "link": "https://googleee.pl/",
            "visits_count": 0,
            "user_ip": "127.0.0.1",
            "user_agent": "HTTPie/3.1.0"
        },
        {
            "shortened_link": "http://127.0.0.1:8000/LcF3m",
            "link": "https://go.pl/",
            "visits_count": 5,
            "user_ip": "127.0.0.1",
            "user_agent": "HTTPie/3.1.0"
        },
        {
            "shortened_link": "http://127.0.0.1:8000/6dYLi",
            "link": "https://gffo.pl/",
            "visits_count": 1,
            "user_ip": "127.0.0.1",
            "user_agent": "HTTPie/3.1.0"
        }
    ]
```

### GET /TZjUn
Redirects to the page assigned to the shortened link.

### GET /TZjUn/info
Show short link info.
#### Response
```json
    {
        "shortened_link": "http://127.0.0.1:8000/LcF3m",
        "link": "https://go.pl/",
        "visits_count": 5,
        "user_ip": "127.0.0.1",
        "user_agent": "HTTPie/3.1.0"
    }
```

### POST /

#### Parameters
```json
    {
        "link": "https://github.com"
    }
```

#### Response
```json
    {
        "shortened_link": "http://127.0.0.1:8000/AqeNG",
        "link": "http://github.com/",
        "visits_count": 0,
        "user_ip": "127.0.0.1",
        "user_agent": "HTTPie/3.1.0"
    }
```