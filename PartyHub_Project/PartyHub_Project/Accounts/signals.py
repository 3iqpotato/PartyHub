import threading
import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


def send_email(subject, message, recipient_email):
    send_mail(
        subject,
        message,
        'your_email@example.com',  # Replace with your actual email
        [recipient_email],
    )


def send_email_thread(subject, message, recipient_email):
    time.sleep(30)
    print('ops')
    send_mail(
        subject,
        message,
        'your_email@example.com',  # Замени с твоя имейл
        [recipient_email],
    )


# Сигнал за изпращане на имейл след регистрация на нов потребител
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_welcome_email_signal(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Party Hub – Where the Fun Never Stops!"

        message = """🎉 Welcome to Party Hub, the place where the party never ends...
                   unless you need to sleep, but we'll understand. 🛏️
                   We're excited to have you here! Get ready for unforgettable moments, crazy events, and memories you'll
                   probably forget (but hey, that's what parties are for, right?). 🕺💃
                   Make sure your dance shoes are ready and your snack game is strong – let's get this party started! 🎊"""

        # Създаване на нова нишка за изпращане на имейла
        thread = threading.Thread(
            target=send_email_thread,
            args=(subject, message, instance.email)
        )
        thread.start()
