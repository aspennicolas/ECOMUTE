from fastapi import APIRouter, Depends

from src.security import require_role

# All routes here will start with /admin, be grouped under "Admin" in the API docs, and require the user to have the "admin" role. The require_role("admin") dependency will check the user's role and raise a 403 error if they don't have the required role.
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_role("admin"))], 
)

# This route is just an example to show that it's protected by the admin role requirement. In a real application, you would replace this with actual admin functionality.
@router.get("/stats")
async def get_admin_stats():
    return {"status": "ok", "message": "Protected admin stats"}