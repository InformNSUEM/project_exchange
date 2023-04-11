from django import forms
from .models import ApplicationAuthority, CustomerGoal, DepthTask, KeyWords, Program


class ApplicationAuthorityForm(forms.ModelForm):
    
    task_formulation = forms.CharField(label="Формулировка задачи",widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    purpose = forms.ModelMultipleChoiceField(label = "Целеполагание", required=True, queryset = CustomerGoal.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': ' form-control' 'form-check-input', 'style': 'margin-top:10px;'}))
    problem_formulation = forms.CharField(label="Формулировка проблемы",widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    relevance = forms.CharField(label="Актуальность", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    depthTask = forms.ModelMultipleChoiceField(label = "Глубина проработки задачи", required=True, queryset = DepthTask.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control' 'form-check-input', 'style': 'margin-top:10px;'}))
    completion_dates = forms.DateField(label = "Сроки завершения работы над задачей",required=True, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    research_purpose = forms.CharField( label="Цель будущего исследования",max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    research_objectives = forms.CharField(label="Задачи исследования", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    key_words = forms.ModelMultipleChoiceField(label = "Ключевые слова", queryset = KeyWords.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'js-example-basic-multiple form-control', 'multiple': 'multiple'}))
    program = forms.ModelMultipleChoiceField(label = "Направления, специальности", queryset = Program.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'js-example-basic-multiple form-control', 'multiple': 'multiple'}))
    wish_result = forms.CharField(label="Ожидаемый результат",max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    other_info = forms.CharField(label="Прочая информация", required = False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))

    class Meta:

        model = ApplicationAuthority
        fields =  ('task_formulation', 'purpose', 'problem_formulation','relevance', 'depthTask', 'completion_dates', 'research_purpose', 'research_objectives',
                   'key_words', 'program','wish_result','other_info' )
        
