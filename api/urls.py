from django.urls import path
from .views import SpringView, PointView

from . import views

urlpatterns = [
  path("springs/", SpringView.as_view(), name= 'spring_list'),
  path("springs/<int:id>", SpringView.as_view(), name= 'spring'),
  path("points/", PointView.as_view(), name= 'point_list'),
  path("points/<int:id>", PointView.as_view(), name= 'points')
]

# urlpatterns = [
#   path("", views.api_home)
# ]