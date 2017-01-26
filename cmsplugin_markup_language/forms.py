####################################################################################################

from django import forms

from .models import MarkupLanguagePluginModel
from .models.MarkupLanguagePluginModel import rst_help_text # Fixme:

####################################################################################################

class MarkupLanguagePluginForm(forms.ModelForm):

    ##############################################

    body = forms.CharField(
                widget=forms.Textarea(attrs={
                    'rows':20,
                    'cols':80,
                    'style':'font-family:monospace'
                }),
                help_text=rst_help_text
            )

    ##############################################

    class Meta:
        model = MarkupLanguagePluginModel
        fields = ["name", "header_level", "body"]
