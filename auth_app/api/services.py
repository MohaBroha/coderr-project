from django.contrib.auth import get_user_model

User = get_user_model()


def create_user_account(validated_data):
    return User.objects.create_user(
        username=validated_data["username"],
        email=validated_data.get("email"),
        password=validated_data["password"],
    )
