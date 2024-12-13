from importlib import import_module
from inspect import getmodule


def present(obj, presenter_class=None):
    """
    This is utility helper for templates or views across the entire codebase.
    This can be now used to create different presenter tags inside the presenter_tag.py file.
    use {obj.__class__.__name__.lower()}_presenter if the presenter will be suffixed with object class name or module
    """
    if presenter_class is None:
        presenter_class = f"{obj.__class__.__name__}Presenter"
        current_module = getmodule(obj).__name__.rsplit(".", 1)[0]
        presenter_module = f"{current_module}.presenter"
        module = import_module(presenter_module)
        presenter_class = getattr(module, presenter_class)
    return presenter_class(obj)
