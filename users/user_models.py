from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
        
        email = models.EmailField(unique=True)
        username = models.CharField(max_length = 30, unique = False)
        patronymic = models.CharField("Отчество", max_length = 100, blank=True, null=True)

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []
        
        def __str__(self) -> str:
            return self.last_name + " " + self.first_name + " " + self.patronymic if self.patronymic else ""
        
        def get_respect_ask(self) -> str:
             
             return self.first_name + " " + self.patronymic
        

        class Meta:
            
            verbose_name = "Пользователь"
            verbose_name_plural = "Пользователи"
