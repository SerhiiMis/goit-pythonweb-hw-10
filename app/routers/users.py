from fastapi import APIRouter, Depends, Request
from app.services.limiter import limiter

from ..auth.dependencies import get_current_user
from ..models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
@limiter.limit("5/minute")
async def get_me(request: Request, current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_verified": current_user.is_verified,
        "avatar_url": current_user.avatar_url,
    }
