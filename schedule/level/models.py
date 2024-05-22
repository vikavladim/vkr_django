from django.db import models


class Level(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='URL', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Параллель'
        verbose_name_plural = 'Параллели'

    def __str__(self):
        return {self.name}


class LevelProgram(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name='Параллель')
    discipline = models.ForeignKey('discipline.Discipline', on_delete=models.CASCADE, verbose_name='Дисциплина')
    load = models.IntegerField(verbose_name='Нагрузка', blank=True, null=True)

    class Meta:
        verbose_name = 'Программа параллели'
        verbose_name_plural = 'Программы параллелей'

    def __str__(self):
        return f'{self.level} - {self.discipline} ({self.load} hours)'
