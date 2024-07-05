import uuid
from django.contrib.auth.models import User

def create_user_name():
    slug = uuid.uuid4()
    if User.objects.filter(username=slug).exists():
        return create_user_name()
    else:
        return slug

