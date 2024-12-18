from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, F, Count
from django.utils import timezone

UserProfile = get_user_model()


class PartyManager(models.Manager):
    def get_not_started_parties(self):
        return self.filter(start_time__gte=timezone.now())

    @staticmethod
    def filter_with_query(parties, query):
        # if he is searching for a specific party here we filter it!!!
        if query:
            parties = parties.filter(title__icontains=query)
        return parties

    @staticmethod
    def filter_available_parties(parties):
        now = timezone.now()

        parties = parties.annotate(tickets_count=Count('tickets')).filter(
            Q(registration_deadline__isnull=True, start_time__gt=now) |  # If not deadline
            Q(registration_deadline__gt=now)  # if deadline
        ).filter(available_spots__gt=F('tickets_count')) # if party not full

        return parties


    def get_parties_for_user(self, user, query=None, user_filter=None): # returns public parties and parties of the user friends!!!
        public_parties = self.get_public_parties().select_related('organizer').order_by('organizer')
        if not user.is_authenticated:
            if user_filter == 'available':
                public_parties = self.filter_available_parties(public_parties)
            return self.filter_with_query(public_parties, query) # for not authenticated users are only public parties


        # for authenticated user we filter the parties to remove his parties and he see only public parties
        parties = public_parties.exclude(id__in=user.organized_parties.values_list('id', flat=True))

        if user_filter == 'public':
            return self.filter_with_query(parties, query)

        # here we add his friends parties (people he follows and they follow him back)
        friends_parties = self.none()
        for friend in UserProfile.objects.get_user_friends(user):
            friends_parties |= friend.get_not_started_parties()

        if user_filter == 'friends':
            return self.filter_with_query(friends_parties, query)

        parties |= friends_parties

        if user_filter == 'available': # TODO: Test because not shure if everything will be okey
            parties = self.filter_available_parties(parties)
            parties = parties.exclude(tickets__participant=user) # removing the parties that user already has tickets
            return self.filter_with_query(parties, query)

        return self.filter_with_query(parties, query)

    def get_current_parties_for_user(self, user):
        now = timezone.now()
        return self.filter(organizer=user, start_time__lte=now, end_time__gte=now)

    def get_public_parties(self):
        return self.get_not_started_parties().filter(is_public=True)

    def get_party_by_id(self, party_id):
        return self.filter(id=party_id).first()