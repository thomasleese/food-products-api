import os

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBearer

from .cache import Cache, Product
from .worker import cache_save


app = FastAPI()
cache = Cache()

allowed_bearer_tokens = os.environ["BEARER_TOKENS"].split(",")
bearer_token_scheme = HTTPBearer()


def check_bearer_token(token: str = Depends(bearer_token_scheme)):
    if token.credentials not in allowed_bearer_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@app.get("/{locale}/{code}")
def read_product(
    locale: str, code: str, bearer_token: str = Depends(check_bearer_token)
):
    product = Product(code, locale)

    try:
        response = cache[product]
        cache_save.delay(product.code, product.locale)
    except KeyError:
        response = cache.save(product)

    return response
