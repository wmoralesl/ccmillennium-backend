from rest_framework import serializers
from .models import Payment
# from courses.serializers import EnrollmentSerializer

class PaymentSerializer(serializers.ModelSerializer):
    # data_enrollment = EnrollmentSerializer(source='enrollment', read_only=True)
    course_name = serializers.CharField(source='enrollment.group.course', read_only=True)
    student_name = serializers.CharField(source='enrollment.student.get_full_name', read_only=True)
    class Meta:
        model = Payment
        fields = ['id', 'enrollment', 'payment_date', 'month_paid', 'amount', 'description', 'course_name', 'student_name']

        