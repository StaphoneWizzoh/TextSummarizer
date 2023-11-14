from django import forms

from .models import Summary

class SummaryForm(forms.ModelForm):
    class Meta:
        model = Summary
        fields = ['input_text', 'input_file']
        
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.fields['input_text'].widget.attrs.update({'class':"custom_textarea"})
        self.fields['input_text'].widget.attrs.update({'class':"custom_textarea"})
        
        
    
