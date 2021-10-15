from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='strength_estimator-home'),
    #path("simple_function",view.simple_function)
    path('index', views.index,name='strength_estimator-index'),
    path('about',views.about,name='strength_estimator-about'),
]
