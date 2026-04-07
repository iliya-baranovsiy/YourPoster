__all__ = ("router",)

from aiogram import Router
from .start_handler import router as start_router
from .autoposting_router import router as self_posting_router

router = Router(name=__name__)
router.include_router(start_router)
router.include_router(self_posting_router)
