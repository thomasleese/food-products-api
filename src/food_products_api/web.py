import os

from fastapi import Depends, FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from .cache import Cache, Product, ProductNotFound
from .worker import cache_save


sentry_sdk.init(traces_sample_rate=0.1)

app = FastAPI()
cache = Cache()

allowed_bearer_tokens = os.environ["BEARER_TOKENS"].split(",")
bearer_token_scheme = HTTPBearer()

app.add_middleware(SentryAsgiMiddleware)


def check_bearer_token(token: str = Depends(bearer_token_scheme)):
    if token.credentials not in allowed_bearer_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@app.exception_handler(ProductNotFound)
def product_not_found_exception_handler(request: Request, exc: ProductNotFound):
    return JSONResponse(
        status_code=404,
        content={"message": "Product could not be found."},
    )


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
