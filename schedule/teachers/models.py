from django.db import models

from pytils.translit import slugify

from django.db import models
from django.urls import reverse


class Teacher(models.Model):
    fio = models.CharField(verbose_name='ФИО', max_length=255)
    position = models.CharField(verbose_name='Должность', max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    photo = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True, verbose_name='Фото')
    room = models.PositiveIntegerField(verbose_name='Кабинет', null=True, blank=True)
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateField(auto_now=True, verbose_name='Дата обновления')
    discipline = models.ManyToManyField('discipline.Discipline', blank=True, verbose_name='Предметы')

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'
        ordering = ['fio']

    def get_absolute_url(self):
        return reverse('teacher_read', kwargs={'slug': self.slug})

    def __str__(self):
        return self.fio

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())

        super(Teacher, self).save(*args, **kwargs)

    @property
    def serializable(self):
        return {
            'id': self.id,
            'fio': self.fio,
            'slug': self.slug,
            'str': self.__str__()
        }


# class Subgroup(models.Model):
#     class_id = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Класс')
#     group_number = models.IntegerField(verbose_name='Номер группы')
#     discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='Дисциплина')
#     teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Преподаватель')
#
#     class Meta:
#         verbose_name = 'Подгруппа'
#         verbose_name_plural = 'Подгруппы'
#
#     def __str__(self):
#         return f'{self.class_id} - {self.discipline_id} - Group {self.group_number}'


# class Program(models.Model):
#     cls = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Класс')
#     discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='Дисциплина')
#     load = models.IntegerField(verbose_name='Нагрузка', blank=True, null=True)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Преподаватель',null=True, blank=True)
#
#
#     class Meta:
#         verbose_name = 'Программа'
#         verbose_name_plural = 'Программы'
#
#     def __str__(self):
#         return f'{self.cls} - {self.discipline} ({self.load} hours)'


# class TeacherSubjectClass(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Преподаватель',null=True, blank=True)
#     _class = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Класс')
#     subject = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='Дисциплина')
#
#     class Meta:
#         verbose_name = 'Учитель-Предмет-Класс'
#         verbose_name_plural = 'Учителя-Предметы-Классы'
#         indexes = [
#             models.Index(fields=['_class', 'subject'], name='unique_class_subject'),
#         ]
#
#     def __str__(self):
#         return f'{self.teacher} - {self.subject} - {self._class}'
#
#     def __eq__(self, other):
#         if isinstance(other, TeacherSubjectClass):
#             # Сравниваем поля или атрибуты объектов на равенство
#             return (
#                     self.teacher == other.teacher and
#                     self.subject == other.subject and
#                     self._class == other._class
#             )
#         return NotImplemented

