from django.urls import path

from vacancies.views import VacancyListView, VacancyDetailView, VacancyCreateView, VacancyUpdateView, \
    VacancyDeleteView, VacancyLikeView, user_vacancies

urlpatterns = [
    path('', VacancyListView.as_view()),
    path('<int:pk>/', VacancyDetailView.as_view()),
    path('create/', VacancyCreateView.as_view()),
    path('<int:pk>/update/', VacancyUpdateView.as_view()),
    path('<int:pk>/delete/', VacancyDeleteView.as_view()),
    path('by_user/', user_vacancies),
    path('like/', VacancyLikeView.as_view()),
]
