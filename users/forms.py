from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(UserCreationForm):
    """Форма регистрации"""
    def __init__(self, *args, **kwargs):
        super(CreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "username", "email")
        required_fields = ("first_name", "username", "email")
