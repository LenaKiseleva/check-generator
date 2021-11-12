import os

import pdfkit
from django.conf import settings
from django.template.loader import get_template
from django_rq import job

from api.models import Check, Choice


def render_html(path: str, params: dict):
    template = get_template(path)
    return template.render(params)


@job
def create_pdf_file(id):
    check = Check.objects.get(id=id)
    filename = f"media/pdf/{check.order['id']}_{check.defined_type}.pdf"
    if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'pdf', filename)):
        check.pdf_file.name = filename
        check.status = Choice.RENDERED
        check.save()
        return
    template = f'{check.defined_type.lower()}_check.html'
    context = {'order': check.order}
    html = render_html(template, context)
    pdfkit.from_string(html, filename)
    check.pdf_file.name = filename
    check.status = Choice.RENDERED
    check.save()
