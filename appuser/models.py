from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User, dispatch_uid="create_user_appuser")
def add_appuser(sender, instance, **kwargs):
    try:
        instance.appuser
    except AppUser.DoesNotExist:
        new_appuser = AppUser(
            user=instance
        )
        new_appuser.save()


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'AppUser <pk:{}>: User <pk: {}> {}'.format(
            self.pk,
            self.user.pk,
            self.user.email
        )

    @property
    def has_valid_policy(self):
        return self.policylog_set.filter(policy=Policy.get_current()).exists()


class Policy(models.Model):
    eula = models.TextField()
    privacy_policy = models.TextField()
    created = models.DateTimeField(default=now, null=True, editable=False)
    version = models.AutoField(primary_key=True)
    current = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.current:
            Policy.objects.filter(current=True).exclude(version=self.version).update(current=False)
        super(Policy, self).save(*args, **kwargs)

    @classmethod
    def get_current(cls):
        return cls.objects.get(current=True)

    @property
    def created_display(self):
        return self.created.strftime('%B %d, %Y')


class PolicyLog(models.Model):
    appuser = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(default=now, null=True, editable=False)

    @classmethod
    def fetch(cls, user):
        instance = cls.objects.filter(appuser__user=user)
        if instance.exists():
            instance = instance.first()
        else:
            instance = cls(appuser=user.appuser)
            instance.save()
        return instance
