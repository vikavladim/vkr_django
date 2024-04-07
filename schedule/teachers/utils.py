class DateMixin:
    def get_context_data(self, context, **kwargs):
        context['selected_menu'] = None
        context.update(**kwargs)
        return context
