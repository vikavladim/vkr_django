from django.contrib import admin,messages

from teachers.models import *

# admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Discipline)
admin.site.register(Subgroup)
admin.site.register(Program)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    fields = ('fio', 'photo', 'room', 'slug', 'subject')
    list_display = ('id', 'fio', 'photo', 'room', 'date_create', 'date_update')
    list_display_links = ('id',)
    list_editable = ('fio', 'room')
    ordering = ('fio', 'room')
    actions = ('send_message',)
    search_fields = ('fio',)
    list_filter = ('subject__name','date_create', 'date_update')
    prepopulated_fields = {'slug': ('fio',)}
    filter_horizontal = ('subject',)

    @admin.display(description='Отправить сообщение')
    def send_message(self, request, queryset):
        print('send message to ', queryset)
        self.message_user(request, 'Всё плохо', messages.WARNING)
        # self.message_user(request,'Всё нормально')
