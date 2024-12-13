class BasePresenter:
    """
    This is initializers for object and content view.
    """

    def __init__(self, obj, view_context=None):
        self.obj = obj
        self.view_context = view_context

    def __getattr__(self, attr):
        if attr in self.__class__.__dict__:
            return getattr(self, attr)
