from django.urls import path
from .import views
urlpatterns = [
    path('',views.stories,name ='stories'),
    path('story/<str:pk>',views.story,name = 'story'),
]
