import sys

try:
    from python_presenter.core.presenters.presenter_helper import present

    def present_object(context, obj, presenter_class=None):
        """
        A function to present an object using the specified presenter class.

        Args:
            obj: The object to be presented.
            presenter_class: The presenter class to use. Defaults to a generic presenter.
            context: The template context.

        Returns:
            An instance of the presenter class.
        """
        return present(obj, presenter_class, context=context)

    if "django" in sys.modules:
        try:
            from django import template

            register = template.Library()
            register.simple_tag(takes_context=True)(present_object)
        except ImportError:
            pass
except ImportError:
    present_object = None
