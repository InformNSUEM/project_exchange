from django.db import models
from .user_models import User
from main import models as mainModels
from django.dispatch import receiver



class StudentUser(models.Model):
     
     user = models.OneToOneField(User, verbose_name = "Пользователь", on_delete = models.CASCADE)
     booknumber = models.BigIntegerField("Номер зачетки", blank = True, null = True)
     dateBith = models.DateField(verbose_name = "Дата рождения", blank=True, null = True)
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