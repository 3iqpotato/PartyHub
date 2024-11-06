from PartyHub_Project.Party.managers import EventManager
from PartyHub_Project.Party.validators import MaxSizeValidator
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

    date = models.DateTimeField(
        blank=False,
        null=False,
        help_text="Set the date and time for the event.",
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
        upload_to='images/', #TODO to make right path to the place to upload the images
        blank=True,
        null=True,
        help_text="Upload an image with a maximum size of 6MB.",
        validators=[MaxSizeValidator(6)]
    )

    registration_deadline = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Optional: Deadline for participant registration.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text="URL-friendly identifier based on the title."
     )

    ended = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if self.date < timezone.now():
            raise ValidationError("The event date cannot be in the past.")

        if self.registration_deadline and self.registration_deadline > self.date:
            raise ValidationError("The registration deadline cannot be after the event date.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    objects = EventManager()

    class Meta:
        ordering = ['-date']

