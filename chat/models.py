from django.db import models
from django.contrib.auth.models import User as User
from django.utils import timezone
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.fields import Field
from django.db.models import Lookup


class NotEqual(Lookup):
    lookup_name = 'ne'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params


Field.register_lookup(NotEqual)


class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=False)
    text = models.TextField(null=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def is_recent(self):
        return self.timestamp >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.text


class UserPresence(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(auto_now=True)

    def is_online(self):
        if self.last_seen is None:
            return False
        else:
            return timezone.now() < \
                self.last_seen + datetime.timedelta(minutes=1)

    def __lt__(self, other):
        return self.last_seen.__lt__(other.last_seen)

    def __gt__(self, other):
        return self.last_seen.__gt__(other.last_seen)


def update_last_seen_time(user):
    user.userpresence.last_seen = timezone.now()
    user.userpresence.save()


@receiver(post_save, sender=User)
def user_updated(sender, **kwargs):
    if (kwargs['created']):
        p = UserPresence(user=kwargs['instance'])
        p.save()
        sender.userpresence = p
