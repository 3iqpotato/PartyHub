from PartyHub_Project.Questions import views
from django.urls import path

urlpatterns = [
    path('question_create/<slug:party_slug>/', views.ask_question, name='question_create'),
    path('answer_create/<int:question_id>/<slug:party_slug>/', views.answer_question, name='answer_create'),
    path('delete_question/<int:pk>/<slug:party_slug>/', views.QuestionDeleteView.as_view(), name='delete_question'),
    path('delete_party/<int:pk>/<slug:party_slug>/', views.AnswerDeleteView.as_view(), name='delete_answer'),
]
