from datetime import datetime
from django.db import models

from django.db import models, transaction
from django.urls.base import reverse
from pytils.translit import slugify

from program.models import Program


class Class(models.Model):
    digit = models.IntegerField(verbose_name='Цифра')
    letter = models.CharField(max_length=1, verbose_name='Буква')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL', db_index=True)
    program = models.ForeignKey('program.Program', on_delete=models.CASCADE, verbose_name='Параллель', blank=True)

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ['digit', 'letter']


    def __str__(self):
        return f'{self.digit}{self.letter}'

    def save(self, *args, **kwargs):
        # if not self.slug:
        self.slug = slugify(self.__str__())
        if not self.program:
            print('hello')
            with transaction.atomic():
                self.program = Program.objects.create(digit=self.digit,
                                             name=f'Индивидуальная программа для {self.digit + self.letter} от {datetime.datetime.now()}')
                print(self.program)
        else:
            print('hello2')
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

