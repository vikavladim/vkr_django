class DateMixin:
    title=None
    extra_context = {}

    def __init__(self):
        if self.title:
            self.extra_context['title'] = self.title

    def get_mixin_context(self, context, **kwargs):
        context['selected_menu'] = None
        context.update(**kwargs)
        return context
