# Makes handlers a package
from .menu import register_menu_handler
from .admin import register_admin_handler


def register_all_handlers(application):
    """Register all bot handlers (customer + admin)."""
    # Customer side
    register_menu_handler(application)

    # Admin side
    register_admin_handler(application)
