from django.forms import ModelForm
from forms_builder.forms.models import Form


class ClientForm(ModelForm):
    class Meta:
        model = Form
        fields = '__all__'
