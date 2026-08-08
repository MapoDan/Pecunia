from fastapi import FastAPI

app = FastAPI(title="Pecunia API", version="0.1.0")


@app.get("/health/live", tags=["health"])
def live() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready", tags=["health"])
def ready() -> dict[str, str]:
    # Database readiness will be wired in with the first migration slice.
    return {"status": "ok"}
