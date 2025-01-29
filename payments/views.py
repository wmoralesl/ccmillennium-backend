from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
import calendar

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['enrollment__student']



@api_view(['GET'])
def generate_pdf(request, id):
    try:
        payment = Payment.objects.get(id=id)
        course_name = payment.enrollment.group.course.name
        student_name = payment.enrollment.student.get_full_name()

        # Lista de nombres de meses en español
        meses_espanol = [
            "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        month_name = meses_espanol[payment.month_paid]

        # Renderizar el template con los datos del pago
        html_string = render_to_string('payment_template.html', {
            'payment': payment,
            'course_name': course_name,
            'student_name': student_name,
            'month_name': month_name
        })

        # Crear el PDF
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        # Crear la respuesta
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="payment_{id}.pdf"'
        return response
    except Payment.DoesNotExist:
        return HttpResponse(status=404)