import re
from .models import ApplicationBuisness
from django.db import models


class Validator:

    def __init__(self, form_data:dict, model) -> None:

        self.model = model
        self.errors = {}
        self.form_data = form_data
        self.required_fields = []


    def get_required_fields(self):

        for field in self.model._meta.many_to_many:
            if not field.blank:
                 self.required_fields.append(field.name)
        
        for field in self.model._meta.fields:
            if not field.blank:
                 self.required_fields.append(field.name)


    def check_required_fields(self):

        self.get_required_fields()

        for key in self.required_fields:

            if key not in self.required_fields or not self.form_data.get(key):
                self.errors[key] = "Поле обязательно для заполнения."
        
        

class BuisnessAppValidator(Validator):

    def __init__(self, form_data: dict, model) -> None:
        super().__init__(form_data, model)

        self.non_required_fields = ["phone_number", "research_purpose", "key_words", "program", "wish_result", "other_info"]

    
    def check_email(self):

        email_pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
        
        if "email" not in self.errors:
             if not re.match(email_pattern, str(self.form_data["email"])):
                self.errors["email"] = "Введите корректный email адрес."

    
    def check_length(self):
        
        length_params = {
            "customer": 150,
            "department": 150,
            "fio": 150,
            "phone_number": 17,
            "key_words": 150,
            "wish_result": 150
        }

        for k, v in length_params.items():

            if k not in self.errors:
                if self.form_data.get(k):
                    if len(self.form_data[k]) > v:
                        self.errors[k] = f"Максимальное число символов может быть {v}"
        
    
    def validate(self):

        self.check_required_fields()
        self.check_email()
        self.check_length()

        is_valid = False if self.errors else True
        

        

        return is_valid, self.errors

        



        

