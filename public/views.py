from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from users.models import User
from courses.models import Course, Group
from payments.models import Payment
from django.utils.timezone import now
from rest_framework.decorators import api_view



@api_view(['GET'])
def dashboard_data(request):
    # Datos de totales
    total_users = User.objects.count()
    total_courses = Course.objects.count()
    total_groups = Group.objects.count()
    total_payments = Payment.objects.count()

    # Usuarios registrados por mes (últimos 6 meses)
    current_month = now().month
    users_per_month = []
    months_labels = []

    for i in range(6):
        month = (current_month - i) % 12 or 12
        year = now().year - ((current_month - i - 1) // 12)
        users_count = User.objects.filter(date_joined__month=month, date_joined__year=year).count()
        users_per_month.append(users_count)
        months_labels.append(now().replace(month=month).strftime('%B'))  # Etiquetas de meses en formato de texto

    # Estudiantes por curso
    courses_distribution = Course.objects.annotate(
        student_count=Count('group__enrollment')
    ).values('name', 'student_count')

    course_labels = [item['name'] for item in courses_distribution]
    course_data = [item['student_count'] for item in courses_distribution]

    data = {
        'total_users': total_users,
        'total_courses': total_courses,
        'total_groups': total_groups,
        'total_payments': total_payments,
        'users_per_month': users_per_month,   # Datos para el gráfico de usuarios por mes
        'months_labels': months_labels,       # Etiquetas de los meses
        'course_labels': course_labels,       # Etiquetas de los cursos
        'course_data': course_data,           # Datos para el gráfico de estudiantes por curso
    }

    return Response(data)
