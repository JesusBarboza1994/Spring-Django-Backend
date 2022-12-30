from django.urls import path
from .views import SpringView

from . import views

urlpatterns = [
  path("springs/", SpringView.as_view(), name= 'spring_list'),
  path("springs/<int:id>", SpringView.as_view(), name= 'spring'),
]

# urlpatterns = [
#   path("", views.api_home)
# ]