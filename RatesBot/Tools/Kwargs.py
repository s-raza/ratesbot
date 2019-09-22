class Kwargs(object):

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

    def init_kwarg(self, to_init, **kwargs):

        if kwargs.get('default') is not None:
            default = kwargs['default']
        else:
            default = None

        return self.kwargs[to_init] if self.kwargs.get(to_init) is not None else default