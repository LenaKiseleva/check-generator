from django.urls import path

from .views import CreateChecksAPIView, NewChecksAPIView, PDFChecksAPIView

urlpatterns = [
    path(
        'create_checks/',
        CreateChecksAPIView.as_view(),
        name='create_checks',
    ),
    path(
        'new_checks/',
        NewChecksAPIView.as_view(),
        name='new_checks',
    ),
    path(
        'check/',
        PDFChecksAPIView.as_view(),
        name='check',
    ),
]
