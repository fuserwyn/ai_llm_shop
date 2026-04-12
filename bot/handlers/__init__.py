from .new_command import router as new_command_router
from .start import router as start_router
from .help import router as help_router

handlers = [
    start_router,
    help_router,
    new_command_router
]