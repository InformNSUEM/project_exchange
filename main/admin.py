from django.contrib import admin
from .models import University, Department, Group, Disciplines, KeyWords, DepthTask, DepthTaskState, EduLevel, FormatResult, CustomerGoal, PackageRequest, InternalApplication, ApplicationAuthority, PackageRequestProcessing, InternalApplicationProcessing, ApplicationAuthorityProcessing, CustomerType, Customer

# Register your models here.
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):

    list_display = ("name" ,"short_name")

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = ("name" ,"short_name", "head_fio", "university")

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(Disciplines)
class DisciplinesAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(KeyWords)
class KeyWordsAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(DepthTask)
class DepthTaskAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(DepthTaskState)
class DepthTaskStateAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(EduLevel)
class EduLevelTaskAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(FormatResult)
class FormatResultAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = ("name", "url", "surname", "name_person", "patronymic", "customerType")

@admin.register(CustomerType)
class CustomerTypeAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(CustomerGoal)
class CustomerGoalAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(PackageRequest)
class PackageRequestAdmin(admin.ModelAdmin):

    list_display = ("theme", "customer", "description", "stages", "wishes")


@admin.register(InternalApplication)
class InternalApplicationAdmin(admin.ModelAdmin):

    list_display = ("theme", "customer",  "relevance", "research_purpose", "research_objectives")

@admin.register(ApplicationAuthority)
class ApplicationAuthorityAdmin(admin.ModelAdmin):

    list_display = ("customer",  "department_authority", "authority_fio", "authority_post", "phone_number", "mail", "task_formulation", "problem_formulation", "relevance", "completion_dates", "research_purpose", "research_objectives", "programm", "wish_result", "other_info")


@admin.register(PackageRequestProcessing)
class PackageRequestProcessingAdmin(admin.ModelAdmin):

    list_display = ("application", "theme",  "completion_dates", "research_purpose", "comment")

@admin.register(InternalApplicationProcessing)
class InternalApplicationProcessingAdmin(admin.ModelAdmin):

    list_display = ("application", "theme",  "completion_dates", "research_purpose", "comment")

@admin.register(ApplicationAuthorityProcessing)
class ApplicationAuthorityProcessingAdmin(admin.ModelAdmin):

    list_display = ("application", "theme",  "completion_dates", "research_purpose", "comment")