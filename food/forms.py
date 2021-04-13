from django.forms import ModelForm
from forms_builder.forms.models import Field


class ClientForm(ModelForm):
    class Meta:
        model = Field
        fields = '__all__'
