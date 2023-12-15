
from exchange.celery import app
from .mail import send_request_approve, send_buisness_request_approve
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