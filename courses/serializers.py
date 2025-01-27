from rest_framework import serializers
from .models import Course, Group, Module, Enrollment


class CourseSerializer(serializers.ModelSerializer):
    group_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'photo', 'monthly_fee', 'total_payments', 'enrollment_fee', 'is_visible', 'is_active', 'group_count']

    def get_group_count(self, obj):
        return obj.group_set.count()

class GroupSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_photo = serializers.ImageField(source='course.photo', read_only=True)
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    teacher_photo = serializers.ImageField(source='teacher.photo', read_only=True)

    class Meta:
        model = Group
        fields = [
            'id', 'name', 'teacher', 'teacher_name', 'year', 'in_person', 'start_date', 'end_date', 
            'schedule', 'hours_count', 'is_visible', 'course', 'course_name', 'is_active', 'teacher_photo', 'course_photo'
        ]


    
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'



class EnrollmentSerializer(serializers.ModelSerializer):
    student_full_name = serializers.CharField(source='student.get_full_name', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    course_name = serializers.CharField(source='group.course.name', read_only=True)
    course_photo = serializers.ImageField(source='group.course.photo', read_only=True)
    student_photo = serializers.ImageField(source='student.photo', read_only=True)
    class Meta:
        model = Enrollment
        fields = ['id', 'student_full_name', 'enrollment_date', 'description', 'amount', 'student', 'group', 'group_name', 
                  'course_name', 'course_photo', 'student_photo'
                  ]


