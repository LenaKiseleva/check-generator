from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models


class Choice(models.Model):
    CHECK_TYPES = [
        (settings.CLIENT, 'client'),
        (settings.KITCHEN, 'kitchen'),
    ]
    CHECK_STATUSES = [
        (settings.NEW, 'new'),
        (settings.RENDERED, 'rendered'),
        (settings.PRINTED, 'printed'),
    ]


class Printer(models.Model):
    name = models.CharField(
        verbose_name='Название принтера',
        max_length=200,
        unique=False,
    )
    api_key = models.CharField(
        verbose_name='Ключ доступа к API',
        max_length=250,
        unique=True,
        blank=False,
        null=False,
    )
    check_type = models.CharField(
        verbose_name='Тип чека который печатает принтер',
        max_length=50,
        choices=Choice.CHECK_TYPES,
    )
    point_id = models.IntegerField(
        verbose_name='Точка к которой привязан принтер'
    )

    class Meta:
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтеры'

    def __str__(self):
        return (
            f'Принтер: {self.name}. '
            f'Тип чека: {self.check_type} '
            f'привязан к точке {self.point_id}'
        )


class Check(models.Model):
    printer_id = models.ForeignKey(
        Printer,
        verbose_name='Принтер',
        on_delete=models.CASCADE,
        related_name='checks',
    )
    defined_type = models.CharField(
        verbose_name='Тип чека',
        max_length=50,
        choices=Choice.CHECK_TYPES,
    )
    order = JSONField(
        verbose_name='Информация о заказе',
    )
    status = models.CharField(
        verbose_name='Статус чека',
        max_length=50,
        choices=Choice.CHECK_STATUSES,
        default=settings.NEW,
    )
    pdf_file = models.FileField(
        verbose_name='Ссылка на созданный PDF-файл',
        max_length=5000,
        upload_to='',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    def __str__(self):
        return (
            f'Чек: {self.id}. '
            f'Тип чека: {self.defined_type} '
            f'от принтера {self.printer_id}'
        )
