[![Build Status](https://github.com/schetininl/foodgram-project/workflows/build/badge.svg)](https://github.com/schetininl/foodgram-project/actions) 
# foodgram-project
foodgram-project

## for local

```
docker-compose -f ./docker-compose.localhost.yml up
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py loaddata ingredients.json
```
