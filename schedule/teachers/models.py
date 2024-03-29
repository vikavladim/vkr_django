from django.db import models

# Create your models here.
from django.db import models

# нужно добавить сокращения предметов
class Teacher(models.Model):
    fio = models.TextField()
    photo = models.ImageField(upload_to='teachers/', null=True)
    room = models.IntegerField()
    date_create = models.DateField(auto_now_add=True)
    date_update = models.DateField(auto_now=True)


class Class(models.Model):
    digit = models.IntegerField()
    letter = models.CharField(max_length=1)


# class Timing(models.Model):
#     class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
#     lesson_number = models.IntegerField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()

class Discipline(models.Model):
    name = models.TextField()


class Subgroup(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    group_number = models.IntegerField()
    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Program(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    load = models.IntegerField()
