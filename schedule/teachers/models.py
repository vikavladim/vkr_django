from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from pytils.translit import slugify

# нужно добавить сокращения предметов
from django.db import models
from django.urls import reverse


class Teacher(models.Model):
    fio = models.CharField(verbose_name='ФИО', max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    photo = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True, verbose_name='Фото')
    room = models.PositiveIntegerField(verbose_name='Кабинет', null=True, blank=True)
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateField(auto_now=True, verbose_name='Дата обновления')
    subject = models.ManyToManyField('Discipline', blank=True, verbose_name='Предметы')

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


class Class(models.Model):
    digit = models.IntegerField(verbose_name='Цифра')
    letter = models.CharField(max_length=1, verbose_name='Буква')
    subject = models.ManyToManyField('Discipline', blank=True, verbose_name='Предметы')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL', db_index=True)

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ['digit', 'letter']

    def __str__(self):
        return f'{self.digit}{self.letter}'

    def save(self, *args, **kwargs):
        # if not self.slug:
        self.slug = slugify(self.__str__())

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


class Discipline(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    short_name = models.CharField(max_length=50, verbose_name='Краткое название',blank=True)
    slug = models.SlugField(max_length=255, verbose_name='URL', unique=True,blank=True, db_index=True)

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ['name',]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.name
        self.slug = slugify(self.__str__())

        super(Discipline, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('subject_read', kwargs={'slug': self.slug})

    @property
    def serializable(self):
        return {
            'id': self.id,
            'name': self.name,
            'short_name': self.short_name,
            'slug': self.slug,
            'str': self.__str__()
        }


class Subgroup(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Класс')
    group_number = models.IntegerField(verbose_name='Номер группы')
    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='Дисциплина')
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Преподаватель')

    class Meta:
        verbose_name = 'Подгруппа'
        verbose_name_plural = 'Подгруппы'

    def __str__(self):
        return f'{self.class_id} - {self.discipline_id} - Group {self.group_number}'


class Program(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Класс')
    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='Дисциплина')
    load = models.IntegerField(verbose_name='Нагрузка')

    class Meta:
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'

    def __str__(self):
        return f'{self.class_id} - {self.discipline_id} ({self.load} hours)'



class TeacherSubjectClass(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Преподаватель')
    _class = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Класс')
    subject = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='Дисциплина')

    class Meta:
        verbose_name = 'Учитель-Предмет-Класс'
        verbose_name_plural = 'Учителя-Предметы-Классы'

    def __str__(self):
        return f'{self.teacher_id} - {self.subject_id} - {self.class_id}'
