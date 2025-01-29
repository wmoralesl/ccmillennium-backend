from django.shortcuts import render
from rest_framework import viewsets
from .models import Assignment, Submission, Content
from .serializers import AssignmentSerializer, SubmissionSerializer, ContentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserSerializer
from courses.models import Enrollment
from rest_framework import status

from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.template.loader import render_to_string
import weasyprint

# Create your views here.
class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']
    
class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'assignment'] 
    

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

class GroupSummaryView(APIView):
    def get(self, request, group_id):
        try:
            # Obtener estudiantes asociados al grupo
            enrollments = Enrollment.objects.filter(group_id=group_id)
            students = [enrollment.student for enrollment in enrollments]
            students_data = UserSerializer(students, many=True).data

            # Obtener tareas asociadas al grupo
            assignments = Assignment.objects.filter(group_id=group_id)
            assignments_data = AssignmentSerializer(assignments, many=True).data

            # Obtener entregas para el grupo específico
            submissions = Submission.objects.filter(assignment__group_id=group_id)
            submissions_data = SubmissionSerializer(submissions, many=True).data

            # Construir la respuesta estructurada
            response_data = {
                "students": students_data,
                "assignments": assignments_data,
                "submissions": submissions_data,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
def generate_pdf_grades(request):
    selected_module_ids = request.data.get("module_ids", [])
    group_id = request.data.get("group_id")
    
    # Filtrar estudiantes y calificaciones de las tareas de los módulos seleccionados
    assignments = Assignment.objects.filter(module__id__in=selected_module_ids, group_id=group_id)
    submissions = Submission.objects.filter(assignment__in=assignments).select_related("student")

    # Organizar los datos en una estructura más fácil de manejar en el template
    students_grades = {}
    for submission in submissions:
        student_id = submission.student.id
        if student_id not in students_grades:
            students_grades[student_id] = {
                "student": submission.student,
                "grades": []
            }
        students_grades[student_id]["grades"].append({
            "assignment": submission.assignment.title,
            "grade": submission.grade or "No calificado",
        })

    # Renderizar el template a HTML
    html_content = render_to_string("pdf_template.html", {"students_grades": students_grades})

    # Generar el PDF usando WeasyPrint
    pdf = weasyprint.HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=calificaciones.pdf"
    return response