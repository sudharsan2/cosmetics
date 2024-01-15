from django.urls import path
from . import views

urlpatterns =[
    path('',views.error_code_response.as_view(),name= 'error_code')
]