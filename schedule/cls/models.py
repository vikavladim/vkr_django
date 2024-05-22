from django.db import models
from django.urls.base import reverse
from pytils.translit import slugify


class Class(models.Model):
    digit = models.IntegerField(verbose_name='Цифра')
    letter = models.CharField(max_length=1, verbose_name='Буква')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL', db_index=True)
    level = models.ForeignKey('level.Level', on_delete=models.CASCADE, verbose_name='Параллель',blank=True)

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ['digit', 'letter']


    def __str__(self):
        return f'{self.digit}{self.letter}'

    def save(self, *args, **kwargs):
        # if not self.slug:
        self.slug = slugify(self.__str__())
        # если не существует такой программы, то создать её

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

    @property
    def serializable(self):
        return {
            'id': self.id,
            'name': self.name,
            'short_name': self.short_name,
            'slug': self.slug,
            'str': self.__str__()
        }

    # def get_absolute_url(self):
    #     return reverse('subject_read', kwargs={'slug': self.slug})


class TeacherSubjectClass(models.Model):
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
        if isinstance(other, TeacherSubjectClass):
            # Сравниваем поля или атрибуты объектов на равенство
            return (
                    self.teacher == other.teacher and
                    self.discipline == other.discipline and
                    self.cls == other.cls
            )
        return NotImplemented
