__all__ = ("router",)

from aiogram import Router
from .adding_channel_handler import router as channel_adding_router

router = Router(name=__name__)
router.include_router(channel_adding_router)
