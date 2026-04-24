from functools import wraps
from ..help_functions.text_functions import error_text
from botLogic.bot_services.app_logging.loggers import autoposting_logger


def async_error_catcher(handler):
    @wraps(handler)
    async def wrapper(*args, **kwargs):
        try:
            return await handler(*args, **kwargs)
        except Exception as e:
            state = kwargs.get('state')
            call = kwargs.get('call') or (args[0] if args else None)
            await state.clear()
            await call.message.edit_text(text=error_text)
            autoposting_logger.info(f'Error {e} в {handler.__name__}')

    return wrapper
