from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='logos/')

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return self.name
