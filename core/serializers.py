from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer, UserSerializer


class UserCreateSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ['id', 'username', 'email',
                  'password', 'first_name', 'last_name']


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
