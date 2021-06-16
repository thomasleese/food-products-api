# Food Products API

**Read and write information about different food products, powered by [Open Food Facts].**

[Open Food Facts]: https://openfoodfacts.org

## Getting started

```sh
pyenv install 3.9.5
poetry install
```

### Running the server

```sh
poetry run uvicorn food_products_api.web:app
```

### Running the tests

```sh
poetry run pytest
```
