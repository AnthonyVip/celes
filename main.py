from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from routes.celes import router as api_router
from routes.auth import router as auth_router
from routes.errors.http_error import http_error_handler
from routes.errors.validation_error import http422_error_handler
from core.settings import settings


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.title,
        description=settings.description,
        version=settings.version,
        debug=settings.debug,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        openapi_url=settings.openapi_url,
        openapi_prefix=settings.openapi_prefix,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(
        HTTPException,
        http_error_handler
    )

    application.add_exception_handler(
        RequestValidationError,
        http422_error_handler
    )

    application.include_router(
        api_router,
        prefix="/datamart",
        tags=["DataMart"]
    )
    application.include_router(
        auth_router,
        prefix="/users",
        tags=["Users"]
    )

    return application


app = get_application()


@app.get("/")
def home():
    return {"Service": "Celes!"}
