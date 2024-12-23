from importlib import import_module
from inspect import getmodule


def present(obj, presenter_class=None):
    """
    Presents an object using either a provided presenter class or auto-discovers
    the appropriate presenter class from the object's module.

    Args:
        obj: The object to be presented
        presenter_class: Optional presenter class to use

    Returns:
        An instance of the presenter class initialized with the object
    """
    if presenter_class is None:
        presenter_class = f"{obj.__class__.__name__}Presenter"
        current_module = getmodule(obj).__name__.rsplit(".", 1)[0]
        presenter_module = f"{current_module}.presenter"
        module = import_module(presenter_module)
        presenter_class = getattr(module, presenter_class)
    return presenter_class(obj)
