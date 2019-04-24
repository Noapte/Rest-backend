Run using Docker
Requirements

    Docker

Steps

    Install Docker
    Clone repository to your local machine
    Navigate to repository's directory in sh
    Type commands to build image and run an app:

docker-compose up -d

    Perform database upgrate / intialization and create user accounts with manage.py script

$ docker-compose exec backend sh
/app# python manage.py db upgrade
/app# python manage.py createuser Admin admin@example.com --admin

on Windows:
before run restart docker desktop 

after first run enter this command in power shell:


Set-NetConnectionProfile -interfacealias "vEthernet (DockerNAT)" -NetworkCategory Private

Then enable drive C,D share in Docker settings.

URL access:

Admin dashboard http://localhost:5000/admin


Open http://localhost:5000/api

1) try to use any command. You should received error.

2) use auth post with your first user credential and get access_token in response body.

3) open 'authorize' and paste authorize token

4) try to use any command e.g. GET /folders/home

5) try to add new folder by POST, get know database etc.

