## How to set up the local environment:
Here's a brief intro about what a developer must do in order to start developing the project further:

- Install the [docker-compose tool](https://docs.docker.com/compose/install/)

- Clone the repo:
```
git clone https://github.com/ivanzorya/e_shop.git
```

- Create .env file based on .env.sample.

- Place .env in the root of the project.

- Run Application:
```
docker-compose -f docker/docker-compose.dev.yml up --build
```

- Setup Admin User:
```
docker exec -it e_shop_web bash
python manage.py createsuperuser
```
- Run tests:
```
docker exec -it e_shop_web bash
python manage.py test
```
- The admin page is available at: http://localhost:8000/admin.
- The api documentation is available at: http://localhost:8000/swagger.

- You're done!
