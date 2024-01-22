
from exchange.celery import app
from .mail import send_request_approve, send_buisness_request_approve
from .models import ApplicationBuisness
from django.db.models import F, Value, DateTimeField, Func, CharField
from django.db.models.functions import Concat, Cast
from django.contrib.postgres.aggregates import StringAgg
from airtable import Airtable
import copy

from celery import shared_task
from exchange.settings import APIKEY, BASEID
@app.task
def send_request_mail(customer_request):
    send_request_approve(customer_request)

@app.task
def send_buisness_request_mail(mail_data):
    send_buisness_request_approve(mail_data)







@shared_task
def update_air():
    package_airtable = Airtable(base_id = BASEID, table_name = "Пакетные заявки", api_key = APIKEY)
    authority_airtable = Airtable(base_id = BASEID, table_name = "Заявки органов власти", api_key = APIKEY)
    nsuem_airtable = Airtable(base_id = BASEID, table_name = "Внутренние заявки НГУЭУ", api_key = APIKEY)
    four_airtable = Airtable(base_id = BASEID, table_name = "Заявки Тип 4", api_key = APIKEY)

    registry_airtable = Airtable(base_id = BASEID, table_name = "Общий реестр 2024", api_key = APIKEY)

    view = "typeX_export"

    data_package = package_airtable.get_all(view= view)



    all_data = {
        "Тема":"",
        "Заказчик": "",
        "Постановка цели исследования": "",
        "Задачи исследования": "",
        "Глубина проработки задачи":"",
        "Ожидаемый результат":"",
        "Тип реестра":""

    }
    all_data_list = list()


    for elem in data_package:
        
        _all_data = copy.deepcopy(all_data)

        _all_data["Тема"] = "" if elem["fields"].get("Тема") == None else elem["fields"]["Тема"]
        _all_data["Заказчик"] = "" if elem["fields"].get("Заказчик") == None else elem["fields"].get("Заказчик")
        _all_data["Постановка цели исследования"] = "" if elem["fields"].get("Описание видения проблемы органами власти") == None else elem["fields"].get("Описание видения проблемы органами власти")
        _all_data["Задачи исследования"] = "" if elem["fields"].get("Предлагаемые этапы проработки (развития) темы") == None else elem["fields"].get("Предлагаемые этапы проработки (развития) темы")
        _all_data["Глубина проработки задачи"] = "" if elem["fields"].get("Пожелания по глубине проработки темы") == None else elem["fields"].get("Пожелания по глубине проработки темы")
        _all_data["Ожидаемый результат"] = "требований к результату нет"
        _all_data["Тип реестра"] = "Пакетные заявки"

        all_data_list.append(_all_data)
        

    data_authority = authority_airtable.get_all(view = view)


    for elem in data_authority:

        _all_data = copy.deepcopy(all_data)
    
        _all_data["Тема"] = "" if elem["fields"].get("Формулировка задачи") == None else elem["fields"]["Формулировка задачи"]
    
        _all_data["Заказчик"] = "" if elem["fields"].get("Заказчик") == None else elem["fields"].get("Заказчик")
        _all_data["Постановка цели исследования"] = "" if elem["fields"].get("Постановка задачи") == None else elem["fields"].get("Постановка задачи")
        _all_data["Задачи исследования"] = "" if elem["fields"].get("Задачи") == None else elem["fields"].get("Задачи")
        _all_data["Глубина проработки задачи"] = "" if elem["fields"].get("_Глубина постановки задачи") == None else elem["fields"].get("_Глубина постановки задачи")
        _all_data["Ожидаемый результат"] = "" if elem["fields"].get("Ожидаемый результат") == None else elem["fields"].get("Ожидаемый результат")
        _all_data["Тип реестра"] = "Заявки органов власти"

        all_data_list.append(_all_data)

    data_nsuem = nsuem_airtable.get_all(view = view)

    for elem in data_nsuem:

        _all_data = copy.deepcopy(all_data)
    
        _all_data["Тема"] = "" if elem["fields"].get("Тема / запрос") == None else elem["fields"]["Тема / запрос"]
    
        _all_data["Заказчик"] = "" if elem["fields"].get("_Заказчик") == None else elem["fields"].get("_Заказчик")
        _all_data["Постановка цели исследования"] = "" if elem["fields"].get("Цель будущего исследования") == None else elem["fields"].get("Цель будущего исследования")
        _all_data["Задачи исследования"] = "" if elem["fields"].get("Задачи исследования") == None else elem["fields"].get("Задачи исследования")
        _all_data["Глубина проработки задачи"] = "" if elem["fields"].get("_Глубина проработки задачи") == None else elem["fields"].get("_Глубина проработки задачи")
        _all_data["Ожидаемый результат"] = "" if elem["fields"].get("Ожидаемый результат") == None else elem["fields"].get("Ожидаемый результат")
        _all_data["Тип реестра"] = "Внутренние заявки НГУЭУ"

        all_data_list.append(_all_data)

    data_four = four_airtable.get_all(view = view)


    for elem in data_four:

        _all_data = copy.deepcopy(all_data)
    
        _all_data["Тема"] = "" if elem["fields"].get("Задача (проблематика)") == None else elem["fields"]["Задача (проблематика)"]
    
        _all_data["Заказчик"] = "" if elem["fields"].get("_Заказчик") == None else elem["fields"].get("_Заказчик")
        _all_data["Постановка цели исследования"] = "" if elem["fields"].get("Цель исследования") == None else elem["fields"].get("Цель исследования")
        _all_data["Задачи исследования"] = "" if elem["fields"].get("Задачи исследования") == None else elem["fields"].get("Задачи исследования")
        _all_data["Глубина проработки задачи"] = "любой"
        _all_data["Ожидаемый результат"] = "" if elem["fields"].get("Ожидаемый результат") == None else elem["fields"].get("Ожидаемый результат")
        _all_data["Тип реестра"] = "Заявки Тип 4"

        all_data_list.append(_all_data)

    
    registry_data = registry_airtable.get_all() 

    record_ids = []

    for elem in registry_data:
        record_ids.append(elem["id"])

    registry_airtable.batch_delete(record_ids = record_ids)

    result = registry_airtable.batch_insert(records = all_data_list)


@shared_task
def update_business():
    
    queryset = (
        ApplicationBuisness.objects.annotate(
        programtitle=StringAgg(Concat('program__code', Value(' '), 'program__name'), delimiter=', ', ordering='program__code'),
        purpose_list=StringAgg('purpose__name', delimiter=', '),
        depthtask=StringAgg('depthTask__name', delimiter=', '),
        completion_date_formatted=Func(
        F('completion_dates'),
        Value('dd.MM.yyyy hh:mm'),
        function='to_char',
        output_field=CharField()
        ),
        created_at_formated=Func(
        F('created_at'),
        Value('dd.MM.yyyy hh:mm'),
        function='to_char',
        output_field=CharField()
        )).values(
        'id',
        'customer',
        'department',
        'fio',
        'post',
        'phone_number',
        'email',
        'purpose_list',
        'task_formulation',
        'problem_formulation',
        'relevance',
        'completion_date_formatted',
        'depthtask',
        'research_purpose',
        'key_words',
        'programtitle',
        'wish_result',
        'other_info',
        )
    )

    registry_airtable = Airtable(base_id = BASEID, table_name = "Коммерческий сектор", api_key = APIKEY)
    registry_data = registry_airtable.get_all() 
    record_ids = []

    for elem in registry_data:
        record_ids.append(elem["id"])
    registry_airtable.batch_delete(record_ids = record_ids)

    insert_data = []

    for obj in queryset:
        insert_data_schema = {}

        insert_data_schema["ID"] = "" if obj.get("id") == None else obj.get("id")
        insert_data_schema["Заказчик"] = "" if obj.get("customer") == None else obj.get("customer")
        insert_data_schema["Структурное подразделение"] = "" if obj.get("department") == None else obj.get("department")
        insert_data_schema["ФИО заказчика"] = "" if obj.get("fio") == None else obj.get("fio")
        insert_data_schema["Должность ответственного от заказчика"] = "" if obj.get("post") == None else obj.get("post")
        insert_data_schema["Телефон ответственного от заказчика"] = "" if obj.get("phone_number") == None else obj.get("phone_number")
        insert_data_schema["Электронная почта ответственного от заказчика"] = "" if obj.get("email") == None else obj.get("email")
        insert_data_schema["Целеполагание заказчика"] = "" if obj.get("purpose_list") == None else obj.get("purpose_list")
        insert_data_schema["Формулировка задачи"] = "" if obj.get("task_formulation") == None else obj.get("task_formulation")
        insert_data_schema["Постановка задачи"] = "" if obj.get("problem_formulation") == None else obj.get("problem_formulation")
        insert_data_schema["Актуальность и источники информации"] = "" if obj.get("relevance") == None else obj.get("relevance")
        insert_data_schema["Глубина проработки задачи"] = "" if obj.get("depthtask") == None else obj.get("depthtask")
        insert_data_schema["Сроки завершения работы над задачей"] = "" if obj.get("completion_date_formatted") == None else obj.get("completion_date_formatted")
        insert_data_schema["Этапы решения задачи"] = "" if obj.get("research_purpose") == None else obj.get("research_purpose")
        insert_data_schema["Ключевые слова"] = "" if obj.get("key_words") == None else obj.get("key_words")
        insert_data_schema["Направления, специальности"] = "" if obj.get("programtitle") == None else obj.get("programtitle")
        insert_data_schema["Ожидаемый результат"] = "" if obj.get("wish_result") == None else obj.get("wish_result")
        insert_data_schema["Прочая информация"] = "" if obj.get("other_info") == None else obj.get("other_info")

        insert_data.append(insert_data_schema)

    result = registry_airtable.batch_insert(records = insert_data)

    

        