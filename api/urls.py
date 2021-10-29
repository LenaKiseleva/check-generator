from django.urls import path

from .views import CreateChecksAPIView, NewChecksAPIView, PDFChecksAPIView

urlpatterns = [
    path(
        'create_checks/',
        CreateChecksAPIView.as_view(),
        name='create_checks',
    ),
    path(
        'new_checks/<str:api_key>/',
        NewChecksAPIView.as_view(),
        name='new_checks',
    ),
    path(
        'check/<str:api_key>/<int:check_id>/',
        PDFChecksAPIView.as_view(),
        name='check',
    ),
]
