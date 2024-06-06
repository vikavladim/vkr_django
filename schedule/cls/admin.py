from django.contrib import admin
from pyexpat.errors import messages

from cls.models import Class

# admin.site.register(Class)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    # fields = ('digit', 'letter', 'subject',)
    # list_display = ('slug', 'digit', 'letter',)
    # list_display_links = ('slug',)
    # list_editable = ('digit', 'letter',)
    # ordering = ('digit', 'letter')
    actions = ('add_year',)
    # search_fields = ('digit', 'letter', 'subject__name',)
    # list_filter = ('digit', 'letter', 'subject__name',)
    # filter_horizontal = ('subject',)
    save_on_top = True

    @admin.display(description='Перевести в следующий класс и выпустить')
    def add_year(self, request, queryset):
        all_classes = queryset.count()

        for obj in queryset:
            obj.digit = obj.digit + 1
            obj.save()

        deleted_count, _ = Class.objects.filter(digit__gt=11).delete()

        if all_classes != 0:
            self.message_user(request, f'Переведено классов: {all_classes - deleted_count}, выпущено: {deleted_count}',
                              messages.SUCCESS)
        else:
            self.message_user(request, 'Никаких классов не переведено', messages.WARNING)

