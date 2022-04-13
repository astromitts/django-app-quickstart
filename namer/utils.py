from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db import IntegrityError
from namer.models import RandomName


def save_anonymous_user(request):
    randomname = RandomName(animals_only=True)
    user = False

    while not user:
        try:
            user = User(
                email='{}@app.tmp'.format(randomname.name),
                username=randomname.name
            )
            user.save()
            login(request, user)
        except IntegrityError:
            user = False
            randomname.get_name()
