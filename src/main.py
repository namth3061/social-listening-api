from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from logging import INFO, Formatter, StreamHandler, getLogger
from driver.nosql import DatabaseConnector
from interfaces.data.const import (
    DEFAULT_TIMEZONE,
    DEFAULT_MAX_AGE_HSTS
)
import secure
import routes.listening_config
from utils.app import check_basic_authentication


def _set_handler(logger, handler):
    handler.setLevel(INFO)
    handler.setFormatter(Formatter(
        '%(name)s: %(funcName)s '
        '[%(levelname)s]: %(message)s'))
    logger.addHandler(handler)
    return logger


logger = getLogger(__name__)
logger = _set_handler(logger, StreamHandler())
logger.setLevel(INFO)
logger.propagate = False

app = FastAPI()

app.include_router(routes.listening_config.router, dependencies=[Depends(check_basic_authentication)])

secure_headers = secure.Secure(
    hsts=secure.StrictTransportSecurity().max_age(DEFAULT_MAX_AGE_HSTS).include_subdomains(),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response


database_connector = DatabaseConnector()


@app.get("/")
async def root(
        db: DatabaseConnector.connect = Depends(database_connector.connect),
        _=Depends(check_basic_authentication),
):
    result = db.urls.find({})
    logger.info('-' * 20 + str(result) + '-' * 20)
    return {"message": "Hello World"}

