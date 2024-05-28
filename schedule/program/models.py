from django.db import models
from pytils.translit import slugify


#сделать мины и максы и прочее
class Program(models.Model):
    digit = models.IntegerField(verbose_name='Параллель')
    name = models.CharField(verbose_name='Название', max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='URL', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Программы'
        verbose_name_plural = 'Программы'

    def __str__(self):
        return f'{self.digit} - {self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())

        super(Program, self).save(*args, **kwargs)


class ProgramDisciplines(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name='Программа')
    discipline = models.ForeignKey('discipline.Discipline', on_delete=models.CASCADE, verbose_name='Дисциплина')
    load = models.IntegerField(verbose_name='Нагрузка', blank=True, null=True)

    class Meta:
        verbose_name = 'Программа и дисциплины'
        verbose_name_plural = 'Программы и дисциплины'

    def __str__(self):
        return f'{self.program} - {self.discipline} ({self.load} часов)'
