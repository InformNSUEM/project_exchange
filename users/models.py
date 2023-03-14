from django.db import models
from django.contrib.auth.models import AbstractUser
from main import models as mainModels
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserType(models.Model):

    name = models.CharField("Наименование", max_length= 100)

    def __str__(self) -> str:
        return self.name

    class Meta:
        
        verbose_name = "Тип пользователя"
        verbose_name_plural = "Тип пользователя"


class User(AbstractUser):
        
        email = models.EmailField(unique=True)
        username = models.CharField(max_length = 30, unique = False)
        dateBith = models.DateField(verbose_name = "Дата рождения", blank=True, null = True)
        patronymic = models.CharField("Отчество", max_length = 100, blank=True, null=True)
        userType = models.ForeignKey(UserType, verbose_name = "Тип пользователя", blank = True, null = True,on_delete = models.CASCADE)

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []
        
        def __str__(self) -> str:
            return self.last_name + " " + self.first_name + " " + self.patronymic if self.patronymic else ""
        

        class Meta:
            
            verbose_name = "Пользователь"
            verbose_name_plural = "Пользователи"


class StudentUser(models.Model):
     
     user = models.OneToOneField(User, verbose_name = "Пользователь", on_delete = models.CASCADE)
     booknumber = models.BigIntegerField("Номер зачетки", blank = True, null = True)
     group = models.ForeignKey(mainModels.Group, verbose_name = "Группа", blank = True, null = True, on_delete = models.CASCADE)

     def __str__(self) -> str:
          return str(self.booknumber)

     class Meta:
          
            verbose_name = "Студент"
            verbose_name_plural = "Студент"


class CustomerUser(models.Model):
     
     user = models.OneToOneField(User, verbose_name = "Пользователь", on_delete = models.CASCADE)
     customer = models.ForeignKey(mainModels.Customer, blank = True, null = True, verbose_name = "Заказчик", on_delete = models.CASCADE)
     post = models.CharField("Должность", blank = True, null = True, max_length = 255)

     def __str__(self) -> str:
          
          return self.user.__str__()
    
     class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчик"

'''
@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
     
     if created and instance.userType.name == "Исполнитель":
          StudentUser.objects.create(
               user = instance,
          )
     else:
          CustomerUser.objects.create(
               user = instance,
          )

'''         