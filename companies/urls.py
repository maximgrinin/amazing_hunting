from django.urls import path

from companies.views import CompanyListView, CompanyImageView

urlpatterns = [
    path('', CompanyListView.as_view()),
    path('<int:pk>/logo/', CompanyImageView.as_view()),
]
