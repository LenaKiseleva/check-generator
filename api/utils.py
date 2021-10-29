import os

import wkhtmltopdf
from django.conf import settings
from django_rq import job

from api.models import Check


@job
def create_pdf_file(id):
    check = Check.objects.get(id=id)
    filename = f"media/pdf/{check.order['id']}_{check.defined_type}.pdf"
    if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'pdf', filename)):
        check.pdf_file.name = filename
        check.status = settings.RENDERED
        check.save()
        return
    rendered_html = f'templates/{check.defined_type.lower()}_check.html'
    wkhtmltopdf.wkhtmltopdf(pages=[rendered_html],
                            output=filename,
                            orientation='Landscape')
    check.pdf_file.name = filename
    check.status = settings.RENDERED
    check.save()
