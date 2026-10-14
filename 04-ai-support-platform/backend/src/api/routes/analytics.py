from fastapi import APIRouter
router = APIRouter(prefix="/analytics", tags=["Analytics"])
@router.get("/dashboard")
async def dashboard(days: int = 30):
    return {"period_days":days,"total_conversations":1247,"escalation_rate":0.12,"avg_resolution_min":4.2,"satisfaction":4.3,"total_cost_usd":18.45,"top_categories":[{"category":"Login","count":342},{"category":"Billing","count":256},{"category":"Feature Request","count":189}]}
