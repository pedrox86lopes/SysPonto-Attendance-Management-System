# attendance/management/commands/create_test_data.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta, time
from django.contrib.auth.hashers import make_password
import random

from core.models import User
from courses.models import Course, ClassSession
from attendance.models import Enrollment, AttendanceCode, AttendanceRecord, AbsenceJustification


class Command(BaseCommand):
    help = 'Creates comprehensive test data for the attendance system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new test data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            AbsenceJustification.objects.all().delete()
            AttendanceRecord.objects.all().delete()
            AttendanceCode.objects.all().delete()
            Enrollment.objects.all().delete()
            ClassSession.objects.all().delete()
            Course.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('✓ Data cleared'))

        self.stdout.write(self.style.WARNING('Creating test data...'))

        # 1. Create Teachers
        teachers_data = [
            {'username': 'prof.silva', 'first_name': 'João', 'last_name': 'Silva', 'email': 'joao.silva@cesae.pt'},
            {'username': 'prof.santos', 'first_name': 'Maria', 'last_name': 'Santos', 'email': 'maria.santos@cesae.pt'},
            {'username': 'prof.costa', 'first_name': 'Pedro', 'last_name': 'Costa', 'email': 'pedro.costa@cesae.pt'},
        ]

        teachers = []
        for teacher_data in teachers_data:
            teacher, created = User.objects.get_or_create(
                username=teacher_data['username'],
                defaults={
                    'first_name': teacher_data['first_name'],
                    'last_name': teacher_data['last_name'],
                    'email': teacher_data['email'],
                    'role': 'teacher',
                    'password': make_password('password123'),
                    'is_staff': True,
                }
            )
            teachers.append(teacher)
            if created:
                self.stdout.write(f'✓ Created teacher: {teacher.username}')

        # 2. Create Students
        students_data = [
            {'username': 'student1', 'first_name': 'Ana', 'last_name': 'Pereira', 'email': 'ana.pereira@student.pt'},
            {'username': 'student2', 'first_name': 'Bruno', 'last_name': 'Oliveira', 'email': 'bruno.oliveira@student.pt'},
            {'username': 'student3', 'first_name': 'Carla', 'last_name': 'Fernandes', 'email': 'carla.fernandes@student.pt'},
            {'username': 'student4', 'first_name': 'David', 'last_name': 'Rodrigues', 'email': 'david.rodrigues@student.pt'},
            {'username': 'student5', 'first_name': 'Eva', 'last_name': 'Martins', 'email': 'eva.martins@student.pt'},
            {'username': 'student6', 'first_name': 'Filipe', 'last_name': 'Almeida', 'email': 'filipe.almeida@student.pt'},
            {'username': 'student7', 'first_name': 'Gabriela', 'last_name': 'Lopes', 'email': 'gabriela.lopes@student.pt'},
            {'username': 'student8', 'first_name': 'Hugo', 'last_name': 'Carvalho', 'email': 'hugo.carvalho@student.pt'},
        ]

        students = []
        for student_data in students_data:
            student, created = User.objects.get_or_create(
                username=student_data['username'],
                defaults={
                    'first_name': student_data['first_name'],
                    'last_name': student_data['last_name'],
                    'email': student_data['email'],
                    'role': 'student',
                    'password': make_password('password123'),
                }
            )
            students.append(student)
            if created:
                self.stdout.write(f'✓ Created student: {student.username}')

        # 3. Create Courses
        courses_data = [
            {'name': 'Desenvolvimento Web Full-Stack', 'code': 'DWFS001', 'description': 'Curso completo de desenvolvimento web'},
            {'name': 'Data Science & Analytics', 'code': 'DSA002', 'description': 'Análise de dados e machine learning'},
            {'name': 'Cybersecurity Fundamentals', 'code': 'CSF003', 'description': 'Fundamentos de cibersegurança'},
            {'name': 'Mobile App Development', 'code': 'MAD004', 'description': 'Desenvolvimento de aplicações móveis'},
        ]

        courses = []
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                code=course_data['code'],
                defaults={
                    'name': course_data['name'],
                    'description': course_data['description'],
                }
            )
            # Assign random teachers to courses
            course.teachers.set(random.sample(teachers, random.randint(1, 2)))
            courses.append(course)
            if created:
                self.stdout.write(f'✓ Created course: {course.name}')

        # 4. Create Enrollments
        for student in students:
            # Each student enrolls in 2-3 random courses
            student_courses = random.sample(courses, random.randint(2, 3))
            for course in student_courses:
                enrollment, created = Enrollment.objects.get_or_create(
                    student=student,
                    course=course
                )
                if created:
                    self.stdout.write(f'✓ Enrolled {student.username} in {course.code}')

        # 5. Create Class Sessions (Past, Current, and Future)
        self.stdout.write('Creating class sessions...')
        
        # Time slots for classes
        time_slots = [
            (time(9, 0), time(12, 0)),   # Morning
            (time(14, 0), time(17, 0)),  # Afternoon
            (time(18, 30), time(21, 30)), # Evening
        ]

        today = timezone.now().date()
        
        # Create sessions for each course
        for course in courses:
            # Past sessions (last 2 weeks)
            for i in range(14, 0, -1):
                session_date = today - timedelta(days=i)
                if session_date.weekday() < 5:  # Only weekdays
                    start_time, end_time = random.choice(time_slots)
                    ClassSession.objects.get_or_create(
                        course=course,
                        date=session_date,
                        start_time=start_time,
                        defaults={'end_time': end_time}
                    )

            # Today's sessions
            if today.weekday() < 5:  # If today is a weekday
                # Morning session (past)
                ClassSession.objects.get_or_create(
                    course=course,
                    date=today,
                    start_time=time(9, 0),
                    defaults={'end_time': time(12, 0)}
                )
                
                # Current session (running now) - IMPORTANT FOR TESTING
                now = timezone.now()
                current_start = (now - timedelta(minutes=30)).time()
                current_end = (now + timedelta(hours=2)).time()
                
                ClassSession.objects.get_or_create(
                    course=course,
                    date=today,
                    start_time=current_start,
                    defaults={'end_time': current_end}
                )
                
                # Future session (tonight)
                ClassSession.objects.get_or_create(
                    course=course,
                    date=today,
                    start_time=time(18, 30),
                    defaults={'end_time': time(21, 30)}
                )

            # Future sessions (next 2 weeks)
            for i in range(1, 15):
                session_date = today + timedelta(days=i)
                if session_date.weekday() < 5:  # Only weekdays
                    start_time, end_time = random.choice(time_slots)
                    ClassSession.objects.get_or_create(
                        course=course,
                        date=session_date,
                        start_time=start_time,
                        defaults={'end_time': end_time}
                    )

        self.stdout.write(f'✓ Created class sessions')

        # 6. Create Attendance Codes (for current sessions)
        current_sessions = ClassSession.objects.filter(
            date=today,
            start_time__lte=timezone.now().time(),
            end_time__gte=timezone.now().time()
        )
        
        for session in current_sessions:
            code, created = AttendanceCode.objects.get_or_create(
                class_session=session,
                defaults={
                    'code': ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6)),
                    'expires_at': timezone.now() + timedelta(minutes=10),
                    'generated_by': session.course.teachers.first(),
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f'✓ Created attendance code: {code.code} for {session.course.name}')

        # 7. Create Attendance Records (some students attended past classes)
        past_sessions = ClassSession.objects.filter(date__lt=today)
        
        for session in past_sessions:
            enrolled_students = User.objects.filter(
                role='student',
                student_enrollments__course=session.course
            )
            
            # 70% of students attended each past session
            attending_students = random.sample(
                list(enrolled_students), 
                int(len(enrolled_students) * 0.7)
            )
            
            for student in attending_students:
                record, created = AttendanceRecord.objects.get_or_create(
                    class_session=session,
                    student=student,
                    defaults={
                        'is_present': True,
                        'simulated_ip': f'192.168.1.{random.randint(1, 254)}',
                        'simulated_geolocation': {
                            'latitude': 41.5369 + random.uniform(-0.01, 0.01),
                            'longitude': -8.4239 + random.uniform(-0.01, 0.01),
                        },
                        'ai_result': {
                            'isFraudulent': random.choice([True, False]) if random.random() < 0.1 else False,
                            'fraudExplanation': 'Location validation passed' if random.random() > 0.1 else 'Suspicious location detected'
                        }
                    }
                )

        # 8. Create Sample Absence Justifications
        try:
            # Get some past sessions without attendance
            sessions_to_justify = []
            for session in past_sessions[:5]:  # Last 5 past sessions
                enrolled_students = User.objects.filter(
                    role='student',
                    student_enrollments__course=session.course
                )
                for student in enrolled_students:
                    # If student didn't attend, create a justification
                    if not AttendanceRecord.objects.filter(class_session=session, student=student).exists():
                        sessions_to_justify.append((session, student))
                        if len(sessions_to_justify) >= 3:  # Create 3 sample justifications
                            break
                if len(sessions_to_justify) >= 3:
                    break

            justification_texts = [
                "Consulta médica urgente. Anexo comprovativo médico.",
                "Falecimento na família. Não pude comparecer à aula.",
                "Problema de transporte devido a greve dos transportes públicos."
            ]

            for i, (session, student) in enumerate(sessions_to_justify):
                AbsenceJustification.objects.get_or_create(
                    student=student,
                    class_session=session,
                    defaults={
                        'description': justification_texts[i % len(justification_texts)],
                        'status': random.choice(['pending', 'approved', 'rejected']),
                        'justification_type': 'absence',
                    }
                )
                self.stdout.write(f'✓ Created justification for {student.username}')

        except Exception as e:
            self.stdout.write(f'Note: Could not create justifications (model may not exist): {e}')

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('✓ TEST DATA CREATION COMPLETE!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'Teachers: {User.objects.filter(role="teacher").count()}')
        self.stdout.write(f'Students: {User.objects.filter(role="student").count()}')
        self.stdout.write(f'Courses: {Course.objects.count()}')
        self.stdout.write(f'Class Sessions: {ClassSession.objects.count()}')
        self.stdout.write(f'Enrollments: {Enrollment.objects.count()}')
        self.stdout.write(f'Attendance Codes: {AttendanceCode.objects.count()}')
        self.stdout.write(f'Attendance Records: {AttendanceRecord.objects.count()}')
        
        try:
            self.stdout.write(f'Absence Justifications: {AbsenceJustification.objects.count()}')
        except:
            self.stdout.write('Absence Justifications: N/A (model not available)')

        self.stdout.write(self.style.SUCCESS('\nLogin credentials:'))
        self.stdout.write('Teachers: prof.silva / prof.santos / prof.costa')
        self.stdout.write('Students: student1 / student2 / ... / student8')
        self.stdout.write('Password for all: password123')
        self.stdout.write(self.style.SUCCESS('\nCurrent running classes are available for late arrival testing!'))