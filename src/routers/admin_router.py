from fastapi import APIRouter, Depends, Header, HTTPException, status

def verify_admin_key(api_key: str = Header(...)) -> None:
    if api_key != "eco-admin-secret":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin API key",
        )

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(verify_admin_key)],
)

@router.get("/stats")
def get_admin_stats():
    return {"status": "ok", "message": "Protected admin stats"}