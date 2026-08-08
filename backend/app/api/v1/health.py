from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Service health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "api"}
