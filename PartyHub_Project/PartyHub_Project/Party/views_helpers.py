from django.utils import timezone

from PartyHub_Project.Questions.forms import AnswerForm, QuestionForm


def check_party_started_and_request_user_is_organizer(party, user):
    return user == party.organizer and party.start_time > timezone.now()

def test_user_can_see_party_details(party, request):
    now = timezone.now()
    if party.end_time <= now:
        return False

    if not party.is_public:
        user = request.user

        if not user.is_authenticated:
            return False

        organizer = party.organizer

        if organizer == user:
            return True

        if not (user.is_following(organizer) and organizer.is_following(user)):
            return False

    return True

def update_context_and_get_status_for_party_details(request, party, context):
    status = False

    if request.user.is_authenticated:

        context['question_form'] = QuestionForm()  # adding form hor authenticated users to ask questions

        # getting the status for the user to see why he can/cant biy ticket for the party!!
        match True:
            case True if party.organizer == request.user:  # if the user is creator of the party
                context['question_form'] = None  # removing the question form
                context['answer_form'] = AnswerForm()  # adding form for answers
                status = "owner"

            case True if party.tickets.filter(participant=request.user):
                status = "have_ticket"  # the user already have a ticket

            case True if party.get_free_spots() == 0:
                status = "no_spots"  # the party is full all tickets are sold

            case True if party.not_late_for_tickets() == False:
                status = "late_for_tickets"  # the party deadline or start have passed

            case True if not party.tickets.filter(participant=request.user):
                status = "can_buy"  # means everithing is okey and we can buy a ticket

    context['status'] = status
    return context