__all__ = ("router",)

from aiogram import Router
from .autoposting_menu import router as menu_router
from .add_cahnnels_router import router as channel_adding_router
from .pricing_plans_router import router as pricing_plan_router

router = Router(name=__name__)
router.include_router(menu_router)
router.include_router(channel_adding_router)
router.include_router(pricing_plan_router)
