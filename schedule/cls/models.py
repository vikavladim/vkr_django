from datetime import datetime
from django.db import models

from django.db import models, transaction
from django.urls.base import reverse
from pytils.translit import slugify

class Level(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='URL', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Параллель'
        verbose_name_plural = 'Параллели'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())

        super(Level, self).save(*args, **kwargs)


class LevelProgram(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name='Параллель')
    discipline = models.ForeignKey('discipline.Discipline', on_delete=models.CASCADE, verbose_name='Дисциплина')
    load = models.IntegerField(verbose_name='Нагрузка', blank=True, null=True)

    class Meta:
        verbose_name = 'Программа параллели'
        verbose_name_plural = 'Программы параллелей'

    def __str__(self):
        return f'{self.level} - {self.discipline} ({self.load} hours)'




class Class(models.Model):
    digit = models.IntegerField(verbose_name='Цифра')
    letter = models.CharField(max_length=1, verbose_name='Буква')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL', db_index=True)
    level = models.ForeignKey('Level', on_delete=models.CASCADE, verbose_name='Параллель',blank=True)

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ['digit', 'letter']


    def __str__(self):
        return f'{self.digit}{self.letter}'

    def save(self, *args, **kwargs):
        # if not self.slug:
        self.slug = slugify(self.__str__())
        if not self.level:
            with transaction.atomic():
                self.level=Level.create(name=f'Для {self.digit}{self.letter} ({datetime.datetime.now()})')
        super(Class, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('class_read', kwargs={'slug': self.slug})

    @property
    def serializable(self):
        return {
            'id': self.id,
            'digit': self.digit,
            'letter': self.letter,
            'slug': self.slug,
            'str': self.__str__()
        }


    # def get_absolute_url(self):
    #     return reverse('subject_read', kwargs={'slug': self.slug})


class TeacherDisciplineClass(models.Model):
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE, verbose_name='Преподаватель')
    cls = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Класс')
    discipline = models.ForeignKey('discipline.Discipline', on_delete=models.CASCADE, verbose_name='Дисциплина')

    class Meta:
        verbose_name = 'Учитель-Предмет-Класс'
        verbose_name_plural = 'Учителя-Предметы-Классы'
        indexes = [
            models.Index(fields=['cls', 'discipline'], name='unique_class_subject'),
        ]

    def __str__(self):
        return f'{self.teacher} - {self.discipline} - {self.cls}'

    def __eq__(self, other):
        if isinstance(other, TeacherDisciplineClass):
            return (
                    self.teacher == other.teacher and
                    self.discipline == other.discipline and
                    self.cls == other.cls
            )
        return NotImplemented



