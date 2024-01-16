from django.urls import path
from . import views

urlpatterns =[
    path('error_code_response',views.error_code_response.as_view(),name= 'error_code'),
    path('placeholders/',views.place_holders.as_view(),name = 'place_holders')
]