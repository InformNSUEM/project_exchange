from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify
from transliterate import translit
from users.user_models import User
#Справочники заказчика

#Тип заказчика
class CustomerType(models.Model):

    name = models.CharField("Наименование", max_length = 50)

    def __str__(self) -> str:
        return self.name

    class Meta:

        verbose_name = "Тип заказчика"
        verbose_name_plural = "Тип заказчика"

#Заказчик
class Customer(models.Model):
    
    name = models.CharField("Наименование", max_length = 150)
    url = models.URLField("Сайт")
    surname = models.CharField("Фамилия", max_length = 100)
    name_person = models.CharField("Имя", max_length = 100)
    patronymic = models.CharField("Отчество", max_length = 100, null = True, blank = True)
    customerType = models.ForeignKey(CustomerType, verbose_name = "Тип заказчика", on_delete = models.SET_NULL, null = True)

    def __str__(self) -> str:
        return self.name

    def calculateFIO(self):

        return (self.surname + " " + self.name + " " + self.patronymic)

    def calculateShortFio(self):
        
        fio = self.calculateFIO()
        short_fio = fio.split(' ')
        short_fio = f'{short_fio[0]} {short_fio[1][0:1]}.{short_fio[2][0:1]}.'
        return short_fio

    

    class Meta:

        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчик"

#############################################################################

#Справочники вуза

#Университет
class University(models.Model):

    name = models.CharField("Полное наименование", max_length = 255)
    short_name = models.CharField("Сокращенное наименование", max_length = 10)

    def __str__(self) -> str:
        return self.name

    class Meta:

        verbose_name = "Университет"
        verbose_name_plural = "Университет"

#Кафедра/Отдел
class Department(models.Model):

    name = models.CharField("Полное наименование", max_length = 150)
    short_name = models.CharField("Краткое наименование", max_length = 10)
    head_fio = models.CharField("ФИО руководителя" , max_length = 150)
    university = models.ForeignKey(University, verbose_name = "Университет", on_delete = models.CASCADE)

    def __str__(self) -> str:
        return self.name

    class Meta:
        
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделение"

    def calculateShortFio(self):
        
        short_fio = self.head_fio.split(' ')
        short_fio = f'{short_fio[0]} {short_fio[1][0:1]}.{short_fio[2][0:1]}.'
        return short_fio


#Дисциплина
class Disciplines(models.Model):

    name = models.CharField("Наименование", max_length = 255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

#Уровень образования
class EduLevel(models.Model):

    name = models.CharField("Наименование", max_length = 50)

    def __str__(self) -> str:
        return self.name

    class Meta:

        verbose_name = "Уровень образования"
        verbose_name_plural = "Уровень образования"

#Направление подготовки
class Program(models.Model):

    code = models.CharField("Код" ,max_length= 8)
    name = models.CharField("Наименование", max_length=100)
    eduLevel = models.ForeignKey(EduLevel, verbose_name = "Уровень образования", on_delete = models.CASCADE)
    department = models.ManyToManyField(Department, verbose_name = "Ответственное подразделение" , related_name = "program_department")

    def __str__(self) -> str:
        return self.code + " " + self.name

    class Meta:
        
        verbose_name = "Направление подготовки"
        verbose_name_plural = "Направления подготовки"

    def makeProgram(self):

        program = self.code + " " + self.name

        return program
    
#Учебная группа
class Group(models.Model):

    name = models.CharField("Наимнование", max_length = 10)
    program = models.ForeignKey(Program, verbose_name = "Направление подготовки", on_delete = models.CASCADE)

    def __str__(self) -> str:
        return self.name

    class Meta:
        
        verbose_name = "Учебная группа"
        verbose_name_plural = "Учебная группа"




#############################################################################
#Справочники для заявки

#Ключевые слова
class KeyWords(models.Model):

    name = models.CharField("Наименование", max_length = 20)

    def __str__(self) -> str:
        return self.name

    class Meta:

        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"

#Глубина проработки задачи
class DepthTask(models.Model):

    name = models.CharField("Наименование", max_length = 150)

    def __str__(self) -> str:
        return self.name

    class Meta:

        verbose_name = "Глубина проработки задачи"
        verbose_name_plural = "Глубина проработки задачи"

#Глубина постановки задачи
class DepthTaskState(models.Model):

    name = models.CharField("Наименование", max_length = 150)

    def __str__(self) -> str:
        return self.name

    class Meta:

        verbose_name = "Глубина постановки задачи"
        verbose_name_plural = "Глубина постановки задачи"



#Формат предполагаемого результата
class FormatResult(models.Model):

    name = models.CharField("Наименование", max_length = 50)

    def __str__(self) -> str:
        return self.name

    class Meta:

        verbose_name = "Формат предполагаемого результата"
        verbose_name_plural = "Формат предполагаемого результата"

class CustomerGoal(models.Model):

    name = models.CharField("Наименование", max_length = 150) 

    def __str__(self) -> str:
        return self.name

    class Meta:

        verbose_name = "Целеполагание заказчика"
        verbose_name_plural = "Целеполагание заказчика"

#####################################################################

#Заявки

#Пакетная заявка
class PackageRequest(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    theme = models.CharField("Тема", max_length=150)
    customer = models.ForeignKey(Customer, verbose_name = "Заказчик", on_delete = models.CASCADE)
    description = models.TextField("Описание")
    stages = models.TextField("Этапы")
    wishes = models.TextField("Пожелания")

    def __str__(self) -> str:
        return self.theme

    class Meta:

        verbose_name = "Пакетная заявка"
        verbose_name_plural = "Пакетная заявка"

#Внутрянняя заявка

class InternalApplication(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    theme = models.CharField("Тема", max_length=150)
    customer = models.ForeignKey(Customer, verbose_name = "Заказчик", on_delete = models.CASCADE)
    key_words = models.ManyToManyField(KeyWords, verbose_name = "Ключевые слова", related_name = "internalApp_keyWords")
    depthTaskState = models.ManyToManyField(DepthTaskState, verbose_name = "Глубина постановки задачи", related_name = "internalApp_depthTaskState")
    edu_level = models.ManyToManyField(EduLevel, verbose_name = "Уровень образования", related_name = "internalApp_eduLevel")
    format_result = models.ManyToManyField(FormatResult, verbose_name = "Формат результата", related_name = "internalApp_formatResult")
    relevance = models.TextField("Обоснование актуальности")
    research_purpose = models.CharField("Цель будущего исследования", max_length = 255)
    research_objectives = models.TextField("Задачи исследования")
    department = models.ManyToManyField(Department,verbose_name = "Ответственное подразделение", related_name = "internalApp_department" )

    def __str__(self) -> str:
        return self.customer.name

    class Meta:

        verbose_name = "Внутрянняя заявка"
        verbose_name_plural = "Внутрянняя заявка"


#Заявка от органа власти

class ApplicationAuthority(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(User, verbose_name = "Заказчик", on_delete = models.CASCADE)#limit_choices_to={"userType__name": "Заказчик"})
    #department_authority = models.CharField("Структурное подразделение", max_length = 150)
    #authority_fio = models.CharField("ФИО заказчика", max_length = 150)
    #authority_post = models.CharField("Должность ответственного от заказчика", max_length = 150)
    #phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Номер телефона должен быть введен в формате: '+799999999'. Разрешено вводить до 15 символов.")
    #phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name = "Телефон ответственного от заказчика")
    #mail = models.EmailField("Электронная почта ответственного от заказчика") 
    purpose = models.ManyToManyField(CustomerGoal, verbose_name = "Целеполагание заказчика", related_name = 'applicationAuthority_customerGoal')
    task_formulation = models.TextField("Формулировка задачи")
    problem_formulation = models.TextField("Постановка задачи")
    relevance = models.TextField("Актуальность и источники информации")
    depthTask = models.ManyToManyField(DepthTask, verbose_name = "Глубина проработки задачи", related_name = "applicationAuthority_depthTash")
    completion_dates = models.DateField("Сроки завершения работы над задачей")
    research_purpose = models.CharField("Цель будущего исследования", max_length = 255)
    research_objectives = models.TextField("Задачи исследования")
    key_words = models.ManyToManyField(KeyWords, verbose_name = "Ключевые слова", related_name = "applicationAuthority_keyWords")
    program = models.ManyToManyField(Program, verbose_name = "Направления, специальности", related_name = "applicationAuthority_program")
    wish_result = models.CharField("Ожидаемый результат", max_length = 150)
    other_info = models.TextField("Прочая информация", blank=True, null=True)

    def __str__(self) -> str:
        return self.customer.get_full_name()

    class Meta:

        verbose_name = "Заявки органов власти"
        verbose_name_plural = "Заявки органов власти"

    
class ApplicationBuisness(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.CharField(verbose_name = "Заказчик",  max_length = 150 )#limit_choices_to={"userType__name": "Заказчик"})
    department = models.CharField("Структурное подразделение", max_length = 150)
    fio = models.CharField("ФИО заказчика", max_length = 150)
    post = models.CharField("Должность ответственного от заказчика", max_length = 150)
    #phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Номер телефона должен быть введен в формате: '+799999999'. Разрешено вводить до 15 символов.")
    phone_number = models.CharField( max_length=17, blank=True, null=True, verbose_name = "Телефон ответственного от заказчика")
    email = models.EmailField("Электронная почта ответственного от заказчика") 
    purpose = models.ManyToManyField(CustomerGoal, verbose_name = "Целеполагание заказчика", related_name = 'applicationBuisness_customerGoal')
    task_formulation = models.TextField("Формулировка задачи")
    problem_formulation = models.TextField("Постановка задачи")
    relevance = models.TextField("Актуальность и источники информации")
    depthTask = models.ManyToManyField(DepthTask, verbose_name = "Глубина проработки задачи", related_name = "applicationBuisness_depthTash")
    completion_dates = models.DateField("Сроки завершения работы над задачей")
    research_purpose = models.TextField("Этапы решения задачи" ,blank = True, null = True)
    key_words = models.CharField("Ключевые слова", max_length = 150, blank = True, null = True)
    program = models.ManyToManyField(Program, verbose_name = "Направления, специальности", blank = True, related_name = "applicationBuisness_program")
    wish_result = models.CharField("Ожидаемый результат", max_length = 150, blank = True, null = True)
    other_info = models.TextField("Прочая информация", blank=True, null=True)

    def __str__(self) -> str:
        return self.customer

    class Meta:

        verbose_name = "Заявки от коммерческого сектора"
        verbose_name_plural = "Заявки от коммерческого сектора"


#####################################################################

#Обработка заявок

class PackageRequestProcessing(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    application = models.ForeignKey(PackageRequest, verbose_name = "Пакетная заявка", on_delete=models.CASCADE)
    theme = models.CharField("Предложения по корректировке формулировки исходной темы", max_length=150)
    depthTask = models.ManyToManyField(DepthTask, verbose_name = "Глубина проработки задачи", related_name = "packageRequestProcessing_depthTash")
    completion_dates = models.CharField("Сроки завершения работы над задачей", max_length = 20)
    research_purpose = models.CharField("Цель будущего исследования", max_length = 255)
    comment = models.TextField("Комментарий")
    discipline = models.ManyToManyField(Disciplines, verbose_name = "Дисциплина", related_name = "packageRequestProcessing_discipline")
    department  = models.ManyToManyField(Department, verbose_name = "Ответственное за реализацию подразделение", related_name = "packageRequestProcessing_department")
    slug = models.SlugField(unique = True, null = False, blank = False)

    def __str__(self) -> str:
        return self.theme

    
    def save(self, *args, **kwargs): 

        if not self.slug:
            self.slug = slugify(self.theme)

        return super().save(*args, **kwargs)

    class Meta:

        verbose_name = "Обработка пакетных заявок"
        verbose_name_plural = "Обработка пакетных заявок"


class InternalApplicationProcessing(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    application = models.ForeignKey(InternalApplication, verbose_name = "Внутрянняя заявка", on_delete=models.CASCADE)
    theme = models.CharField("Предложения по корректировке формулировки исходной темы", max_length=150)
    depthTask = models.ManyToManyField(DepthTask, verbose_name = "Глубина проработки задачи", related_name = "internalApplicationProcessing_depthTash")
    completion_dates = models.CharField("Сроки завершения работы над задачей", max_length = 20)
    research_purpose = models.CharField("Цель будущего исследования", max_length = 255)
    comment = models.TextField("Комментарий")
    discipline = models.ManyToManyField(Disciplines, verbose_name = "Дисциплина", related_name = "internalApplicationProcessing_discipline")
    department  = models.ManyToManyField(Department, verbose_name = "Ответственное за реализацию подразделение", related_name = "internalApplicationProcessing_department")
    slug = models.SlugField(unique = True, null = True, blank = True)

    def __str__(self) -> str:
        return self.theme

    def save(self, *args, **kwargs): 

        if not self.slug:
            self.slug = slugify(self.theme)

        return super().save(*args, **kwargs)

    class Meta:

        verbose_name = "Обработка внутренних заявок"
        verbose_name_plural = "Обработка внутренних заявок"


class ApplicationAuthorityProcessing(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    application = models.ForeignKey(ApplicationAuthority, verbose_name = "Внутрянняя заявка", on_delete=models.CASCADE)
    theme = models.CharField("Предложения по корректировке формулировки исходной темы", max_length=150)
    depthTask = models.ManyToManyField(DepthTask, verbose_name = "Глубина проработки задачи", related_name = "applicationAuthorityProcessing_depthTash")
    completion_dates = models.CharField("Сроки завершения работы над задачей", max_length = 20)
    research_purpose = models.CharField("Цель будущего исследования", max_length = 255)
    comment = models.TextField("Комментарий")
    discipline = models.ManyToManyField(Disciplines, verbose_name = "Дисциплина", related_name = "applicationAuthorityProcessing_discipline")
    department  = models.ManyToManyField(Department, verbose_name = "Ответственное за реализацию подразделение", related_name = "applicationAuthorityProcessing_department")
    slug = models.SlugField(unique = True, null = True, blank = True)


    def __str__(self) -> str:
        return str(self.theme)

    def save(self, *args, **kwargs): 

        ru_text = self.theme
        text = translit(ru_text, language_code='ru', reversed=True)
        
        if not self.slug:
            self.slug = slugify(text)

        return super(ApplicationAuthorityProcessing, self).save(*args, **kwargs)

    class Meta:

        verbose_name = "Обработка заявок от органов власти"
        verbose_name_plural = "Обработка заявок от органов власти"

