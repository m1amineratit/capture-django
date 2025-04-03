from django.urls import path
from . import views

urlpatterns = [
    path('capture-image/', views.silent_capture_and_upload, name='silent_capture_and_upload'),
    path('capture-page/', views.show_capture_page, name='show_capture_page'),  # Optional, if you want to show a page
]
