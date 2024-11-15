from PartyHub_Project.Party.managers import PartyManager
from PartyHub_Project.Party.validators import MaxSizeValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


# Create your models here.

class Party(models.Model):
    PARTY_TYPES = [
        ('metal', 'Metal'),
        ('rap', 'Rap'),
        ('chalga', 'Chalga'),
        ('disco', 'Disco'),
        ('drinking', 'Drinking'),
        ('drinking_and_smoking', 'Drinking and smoking'),
        ('normal', 'Normal'),
        ('gaming', 'Gaming'),
        ('meetup', 'Meetup'),
        ('other', 'Other'),
    ]

    organizer = models.ForeignKey(
        to=get_user_model(),  # Свързване към модела UserProfile
        on_delete=models.CASCADE,  # Изтриване на събитията при изтриване на потребителя
        related_name='organized_parties',  # Свързване обратно за лесен достъп до събитията
    )

    title = models.CharField(
        max_length=70,
        blank=False,
        null=False,
        unique=True,
        help_text="Enter a unique title of at least 5 characters.",
        validators=[
            MinLengthValidator(5, "The title must be at least 5 characters long."),
        ]
    )

    description = models.TextField(
        blank=False,
        null=False,
        max_length=300,
    )

    start_time = models.DateTimeField(
        blank=False,
        null=False,
        help_text="Set the start date and time for the party.",
    )

    end_time = models.DateTimeField(
        blank=False,
        null=False,
        help_text="Set the end date and time for the party.",
    )

    location = models.TextField(
        max_length=70,
        null=False,
        blank=False,
    )

    party_type = models.CharField(
        max_length=20,
        choices=PARTY_TYPES,
        blank=False,
        null=False,
        help_text="Select an event type, or choose 'Other' to specify your own.",
        validators=[MinLengthValidator(3, "Party type must be at least characters long.")]
    )

    available_spots = models.PositiveIntegerField(
        blank=False,
        null=False,
        help_text="Minimum of 2 people required.",
        validators=[MinValueValidator(2, "Available spots can't be less than 2!")]
    )

    picture = models.ImageField(
        upload_to='party_imgs/', #TODO to make right path to the place to upload the images
        blank=True,
        null=True,
        help_text="Upload an image with a maximum size of 6MB.",
        validators=[MaxSizeValidator(6)]
    )

    registration_deadline = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Optional: Deadline for participant registration.",
    ) #TODO да направя да не излизат партита на който тази дата е минала и други неща с това!!!

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text="URL-friendly identifier based on the title."
     )

    is_public = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )

    def get_free_spots(self):
        return self.available_spots - self.tickets.count()

    def not_late_for_tickets(self):
        now = timezone.now()
        if self.registration_deadline:
            return self.registration_deadline > now
        else:
            return self.start_time > now

    # def clean(self):
    #
    #     super().clean()
    #     if self.start_time < timezone.now():
    #         raise ValidationError("The party start time cannot be in the past.")
    #
    #     if self.end_time <= self.start_time:
    #         raise ValidationError("The end time must be after the start time.")
    #
    #     if self.registration_deadline and self.registration_deadline > self.start_time:
    #         raise ValidationError("The registration deadline cannot be after the party start time.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    objects = PartyManager()

    class Meta:
        ordering = ['-start_time']

