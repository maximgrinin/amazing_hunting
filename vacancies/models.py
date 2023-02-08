from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from authentication.models import User


def check_date_not_past(value: date):
    if value < date.today():
        raise ValidationError('%(value)s is in the past')


class Skill(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    STATUS = [('draft', 'Черновик'),
              ('open', 'Открыта'),
              ('closed', 'Закрыта')]

    slug = models.SlugField(max_length=50)
    text = models.CharField(max_length=2000)
    status = models.CharField(max_length=6, choices=STATUS, default='draft')
    created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    skills = models.ManyToManyField(Skill)
    likes = models.IntegerField(default=0)
    min_experience = models.IntegerField(null=True, validators=[MinValueValidator(0)])
    updated_at = models.DateField(null=True, validators=[check_date_not_past])

    @property
    def username(self):
        return self.user.username if self.user else None

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        # ordering = ["text"]

    def __str__(self):
        return self.slug
