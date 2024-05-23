from django.db import models
from pytils.translit import slugify


class Discipline(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    short_name = models.CharField(max_length=50, verbose_name='Краткое название', blank=True)
    slug = models.SlugField(max_length=255, verbose_name='URL', unique=True, blank=True, db_index=True)

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ['name', ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.name
        self.slug = slugify(self.__str__())

        super(Discipline, self).save(*args, **kwargs)

    @property
    def serializable(self):
        return {
            'id': self.id,
            'name': self.name,
            'short_name': self.short_name,
            'slug': self.slug,
            'str': self.__str__()
        }
