class DateMixin:
    title = None
    selected_menu = None
    paginate_by = 2
    extra_context = {}

    def __init__(self):
        if self.title:
            self.extra_context['title'] = self.title

        if self.selected_menu:
            self.extra_context['selected_menu'] = self.selected_menu

    def get_mixin_context(self, context, **kwargs):
        # context['selected_menu'] = None
        context.update(**kwargs)
        return context
