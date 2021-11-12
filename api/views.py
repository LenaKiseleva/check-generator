import json

import django_rq
from django.db import transaction
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView

from .models import Check, Choice, Printer
from .serializers import ChecksSerializer, CreateChecksSerializer
from .utils import create_pdf_file


class CreateChecksAPIView(CreateAPIView):
    queryset = Check.objects.all()
    serializer_class = CreateChecksSerializer

    @transaction.atomic
    def post(self, request):
        content = json.loads(request.body.decode('utf-8'))
        checks = Check.objects.filter(order__id=content['id']).exists()
        point_id = content.pop('point_id')
        printers = Printer.objects.filter(point_id=point_id)
        if printers:
            if not checks:
                for printer in printers:
                    check = Check.objects.create(
                        printer_id=printer,
                        defined_type=printer.check_type,
                        order=content,
                    )
                    queue = django_rq.get_queue('default')
                    create_pdf_file.delay(check.id)
                return JsonResponse(
                    {'ok': 'Чеки успешно созданы'},
                    status=status.HTTP_200_OK
                )
            return JsonResponse(
                {'error': 'Для данного заказа уже созданы чеки'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return JsonResponse(
            {'error': 'Для данной точки не настроено ни одного принтера'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class NewChecksAPIView(ListAPIView):
    queryset = Check.objects.all()
    serializer_class = ChecksSerializer

    def get(self, request):
        try:
            api_key = request.query_params['api_key']
            printer = get_object_or_404(Printer, api_key=api_key)
            if printer:
                checks = printer.checks.filter(status=Choice.NEW)
                serializer = ChecksSerializer(checks, many=True)
                return JsonResponse(
                    {'checks': serializer.data},
                    status=status.HTTP_200_OK
                )
        except Http404:
            return JsonResponse(
                {'error': 'Ошибка авторизации'},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class PDFChecksAPIView(GenericAPIView):
    queryset = Check.objects.all()
    serializer_class = ChecksSerializer

    def get(self, request):
        api_key = request.query_params['api_key']
        check_id = request.query_params['check_id']
        if not Printer.objects.filter(api_key=api_key).exists():
            return JsonResponse(
                {'error': 'Не существует принтера с таким api_key'},
                status=401
            )
        check = Check.objects.filter(id=check_id).first()
        if not check:
            return JsonResponse(
                {'error': 'Данного чека не существует'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not check.pdf_file:
            return JsonResponse(
                {'error': 'Для данного чека не сгенерирован PDF-файл'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        check.status = Choice.PRINTED
        check.save()
        response = HttpResponse(check.pdf_file, content_type='application/pdf')
        name = check.pdf_file.name
        response['Content-Disposition'] = 'attachment; filename="' + name + '"'
        return response
