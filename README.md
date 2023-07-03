# Intro

* link = https://github.com/team21-movies-services/movies-api

# Init development

1) init poetry and pre-commit
```bash
poetry install --no-root
```

```bash
poetry run pre-commit install
```

2) env
```
cp ./.env.example ./.env
```

3) up docker local
```bash
make up-local
```

4) go = http://localhost/api/openapi

# Testing
```bash
make up-tests
```
