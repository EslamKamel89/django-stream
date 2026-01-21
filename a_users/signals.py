from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from a_users.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(
    post_save,
    sender=User,
    dispatch_uid="sync_user_primary_email",
)
def sync_email_address(sender, instance: User, created, **kwargs):
    if created:
        return
    if not instance.email:
        return
    email_address = EmailAddress.objects.filter(user=instance, primary=True).first()
    if email_address and email_address.email == instance.email:
        return
    EmailAddress.objects.filter(user=instance).update(primary=False, verified=False)
    email_address, _ = EmailAddress.objects.update_or_create(
        user=instance,
        email=instance.email,
        defaults={"primary": True, "verified": False},
    )


@receiver(pre_save, sender=User)
def user_presave(sender, instance: User, **kwargs):
    if instance.username:
        instance.username = instance.username.lower()
