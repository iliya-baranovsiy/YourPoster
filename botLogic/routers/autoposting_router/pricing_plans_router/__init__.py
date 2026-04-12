__all__ = ("router",)

from aiogram import Router
from .pricing_plan_handler import router as price_router

router = Router(name=__name__)
router.include_router(price_router)
