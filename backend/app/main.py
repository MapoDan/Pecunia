from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.auth import router as auth_router
from app.api.v1.expenses import router as expenses_router
from app.api.v1.health import router as health_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    app.include_router(health_router, prefix=settings.api_v1_prefix)
    app.include_router(auth_router, prefix=settings.api_v1_prefix)
    app.include_router(expenses_router, prefix=settings.api_v1_prefix)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = request.headers.get("x-request-id", "unavailable")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Unexpected server error",
                    "request_id": request_id,
                    "details": {},
                }
            },
        )

    return app


app = create_app()
