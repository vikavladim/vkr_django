from django.db import models

# Create your models here.
from django.db import models

# нужно добавить сокращения предметов
class Teacher(models.Model):
    fio = models.TextField(verbose_name='ФИО')
    photo = models.ImageField(upload_to='teachers/', null=True, verbose_name='Фото')
    room = models.IntegerField(verbose_name='Кабинет')
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateField(auto_now=True, verbose_name='Дата обновления')


class Class(models.Model):
    digit = models.IntegerField(verbose_name='Цифра')
    letter = models.CharField(max_length=1, verbose_name='Буква')


# class Timing(models.Model):
#     class_id = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Класс')
#     lesson_number = models.IntegerField(verbose_name='Номер урока')
#     start_time = models.TimeField(verbose_name='Начало')
#     end_time = models.TimeField(verbose_name='Конец')

class Discipline(models.Model):
    name = models.TextField(verbose_name='Название')


class Subgroup(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Класс')
    group_number = models.IntegerField(verbose_name='Номер группы')
    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='Дисциплина')
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Преподаватель')


class Program(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Класс')
    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='Дисциплина')
    load = models.IntegerField(verbose_name='Нагрузка')