from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from teachers.models import *

admin.site.register(Discipline)
# admin.site.register(Subgroup)
admin.site.register(Program)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    fields = ('fio', 'photo', 'post_photo', 'room', 'subject')
    list_display = ('id', 'fio', 'post_photo', 'room', 'date_create', 'date_update')
    list_display_links = ('id',)
    list_editable = ('fio', 'room')
    ordering = ('fio', 'room')
    actions = ('send_message',)
    search_fields = ('fio',)
    list_filter = ('subject__name', 'date_create', 'date_update')
    # prepopulated_fields = {'slug': ('fio',)}
    filter_horizontal = ('subject',)
    readonly_fields = ('post_photo',)
    save_on_top = True

    @admin.display(description='Отправить сообщение')
    def send_message(self, request, queryset):
        print('send message to ', queryset)
        self.message_user(request, 'Всё плохо', messages.WARNING)
        # self.message_user(request,'Всё нормально')

    @admin.display(description='Изображение')
    def post_photo(self, obj: Teacher):
        if not obj.photo:
            return 'Нет фото'
        return mark_safe(f'<img src="{obj.photo.url}" width="50">')


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    fields = ('digit', 'letter', 'subject',)
    list_display = ('slug', 'digit', 'letter',)
    list_display_links = ('slug',)
    list_editable = ('digit', 'letter',)
    ordering = ('digit', 'letter')
    actions = ('add_year',)
    search_fields = ('digit', 'letter', 'subject__name',)
    list_filter = ('digit', 'letter', 'subject__name',)
    filter_horizontal = ('subject',)
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
