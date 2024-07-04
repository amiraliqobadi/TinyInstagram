import django_filters
from user.models import CustomUser


class UserFilter(django_filters.FilterSet):

    class Meta:
        model = CustomUser
        fields = ("user_name",)
