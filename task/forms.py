from task.models import Task
from django import forms


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        ordering = ['-updated_at']
        fields = ['title', 'description', 'is_done', 'is_delete']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 7, 'placeholder': 'Описание...'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_delete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
