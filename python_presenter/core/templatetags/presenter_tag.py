import sys

if "django" in sys.modules:
    try:
        from django import template

        from python_presenter.core.presenters.presenter_helper import present

        register = template.Library()

        @register.simple_tag(takes_context=True)
        def present_object(context, obj, presenter_class=None):
            """
            A template tag to present an object using the specified presenter class.

            Args:
                context: Template context.
                obj: The object to be presented.
                presenter_class: The presenter class to use. Defaults to a generic presenter.

            Returns:
                An instance of the presenter class.
            """
            return present(obj, presenter_class)

    except ImportError:
        raise ImportError("Django is installed but its template system could not be loaded.")
else:
    register = None
