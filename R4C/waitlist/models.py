from django.db import models

from customers.models import Customer


class WaitList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5, blank=False, null=False)


# p.s. Для третьего задания можно было добавить доп.поле в модель Robot
# Но по условию задачи переопределять методы модели нельзя,
# Поэтому получилось создать доп.таблицу для хранения листа ожидания.
