from cloudinary.models import CloudinaryField
from cloudinary.uploader import destroy

from PartyHub_Project.Party.managers import PartyManager
from PartyHub_Project.Party.validators import MaxSizeValidator
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from unidecode import unidecode


# Create your models here.

class Party(models.Model):
    PARTY_TYPES = [
        ('metal', 'Metal'),
        ('rap', 'Rap'),
        ('chalga', 'Chalga'),
        ('disco', 'Disco'),
        ('birthday', 'Birthday'),
        ('wedding', 'Wedding'),
        ('conference', 'Conference'),
        ('drinking', 'Drinking'),
        ('drinking_and_smoking', 'Drinking and smoking'),
        ('gaming', 'Gaming'),
        ('meetup', 'Meetup'),
        ('other', 'Other'),
    ]

    organizer = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='organized_parties',
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

    # picture = models.ImageField(
    #     upload_to='party_imgs/', #TODO to make right path to the place to upload the images
    #     blank=True,
    #     null=True,
    #     help_text="Upload an image with a maximum size of 5MB.",
    #     validators=[MaxSizeValidator(5)]
    # )  # TODO: da se trie starata!!!

    picture = CloudinaryField(
    'image',
        folder="party_imgs",
        blank=True,
        null=True,
        validators=[MaxSizeValidator(5)],
        help_text="Upload an image with a maximum size of 6MB.",)

    registration_deadline = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Optional: Deadline for participant registration.",
    )

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

    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_title = unidecode(self.title)
            self.slug = slugify(transliterated_title)

        # try:
        #     this = Party.objects.get(pk=self.pk)
        #     if this.picture != self.picture and this.picture:
        #         this.picture.delete(save=False)
        # except Party.DoesNotExist:
        #     pass

        try:
        # Fetch the existing object from the database
            this = Party.objects.get(pk=self.pk)
                # Check if the profile picture is changing and is not the same
            if (self.picture and this.picture and this.picture != self.picture
                    and not f'{self.picture}' == f'{this.picture}'):

                destroy(this.picture.public_id)

        except Party.DoesNotExist:
                # No existing object, so nothing to delete
                pass

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    objects = PartyManager()

    class Meta:
        ordering = ['-start_time']

