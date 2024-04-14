from django.contrib import admin,messages
from django.utils.safestring import mark_safe

from teachers.models import *

# admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Discipline)
admin.site.register(Subgroup)
admin.site.register(Program)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    fields = ('fio', 'photo', 'post_photo', 'room', 'slug', 'subject')
    list_display = ('id', 'fio', 'post_photo', 'room', 'date_create', 'date_update')
    list_display_links = ('id',)
    list_editable = ('fio', 'room')
    ordering = ('fio', 'room')
    actions = ('send_message',)
    search_fields = ('fio',)
    list_filter = ('subject__name','date_create', 'date_update')
    prepopulated_fields = {'slug': ('fio',)}
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

# @admin.register(Class)
# class ClassAdmin(admin.ModelAdmin):
#     class Meta:
#         model = Class
#         fields = ['letter', 'slug', 'digit', 'subject']
#         widgets = {
#             'subject': forms.SelectMultiple(attrs={'class': 'filter_horizontal'}),
#         }
