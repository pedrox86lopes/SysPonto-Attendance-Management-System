from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model

from core.models import User
from courses.models import Course, ClassSession
from attendance.models import Enrollment, AttendanceCode, AttendanceRecord, AbsenceJustification


class Command(BaseCommand):
    help = 'Completely cleans the database except for the admin user "pedrox86"'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all data (required for safety)',
        )
        parser.add_argument(
            '--admin-username',
            type=str,
            default='pedrox86',
            help='Username of the admin account to preserve (default: pedrox86)',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.ERROR('⚠️  This command will DELETE ALL DATA except the admin account!')
            )
            self.stdout.write(
                self.style.WARNING('To confirm, run: python manage.py clean_database --confirm')
            )
            return

        admin_username = options['admin_username']
        
        # Verify admin user exists
        try:
            admin_user = User.objects.get(username=admin_username)
            if not admin_user.is_superuser:
                self.stdout.write(
                    self.style.ERROR(f'User "{admin_username}" exists but is not a superuser!')
                )
                return
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Admin user "{admin_username}" not found!')
            )
            return

        self.stdout.write(
            self.style.WARNING(f'🧹 Starting database cleanup...')
        )
        self.stdout.write(
            self.style.WARNING(f'📋 Preserving admin user: {admin_username}')
        )

        # Use transaction to ensure atomicity
        try:
            with transaction.atomic():
                # Step 1: Delete attendance-related data
                self.stdout.write(self.style.HTTP_INFO('🗑️  Deleting absence justifications...'))
                justifications_count = AbsenceJustification.objects.count()
                AbsenceJustification.objects.all().delete()
                self.stdout.write(f'   ✓ Deleted {justifications_count} absence justifications')

                self.stdout.write(self.style.HTTP_INFO('🗑️  Deleting attendance records...'))
                records_count = AttendanceRecord.objects.count()
                AttendanceRecord.objects.all().delete()
                self.stdout.write(f'   ✓ Deleted {records_count} attendance records')

                self.stdout.write(self.style.HTTP_INFO('🗑️  Deleting attendance codes...'))
                codes_count = AttendanceCode.objects.count()
                AttendanceCode.objects.all().delete()
                self.stdout.write(f'   ✓ Deleted {codes_count} attendance codes')

                self.stdout.write(self.style.HTTP_INFO('🗑️  Deleting enrollments...'))
                enrollments_count = Enrollment.objects.count()
                Enrollment.objects.all().delete()
                self.stdout.write(f'   ✓ Deleted {enrollments_count} enrollments')

                # Step 2: Delete course-related data
                self.stdout.write(self.style.HTTP_INFO('🗑️  Deleting class sessions...'))
                sessions_count = ClassSession.objects.count()
                ClassSession.objects.all().delete()
                self.stdout.write(f'   ✓ Deleted {sessions_count} class sessions')

                self.stdout.write(self.style.HTTP_INFO('🗑️  Deleting courses...'))
                courses_count = Course.objects.count()
                Course.objects.all().delete()
                self.stdout.write(f'   ✓ Deleted {courses_count} courses')

                # Step 3: Delete users (except admin)
                self.stdout.write(self.style.HTTP_INFO('🗑️  Deleting users (except admin)...'))
                users_to_delete = User.objects.exclude(username=admin_username)
                users_count = users_to_delete.count()
                users_to_delete.delete()
                self.stdout.write(f'   ✓ Deleted {users_count} users')

                # Verify admin user still exists
                if User.objects.filter(username=admin_username).exists():
                    self.stdout.write(
                        self.style.SUCCESS(f'   ✓ Admin user "{admin_username}" preserved successfully')
                    )
                else:
                    raise Exception(f'Admin user "{admin_username}" was accidentally deleted!')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error during cleanup: {str(e)}')
            )
            self.stdout.write(
                self.style.ERROR('Transaction rolled back - no changes made')
            )
            return

        # Final verification and summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✅ DATABASE CLEANUP COMPLETED SUCCESSFULLY!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        # Show final counts
        self.stdout.write(f'📊 Final database state:')
        self.stdout.write(f'   • Users: {User.objects.count()} (admin only)')
        self.stdout.write(f'   • Courses: {Course.objects.count()}')
        self.stdout.write(f'   • Class Sessions: {ClassSession.objects.count()}')
        self.stdout.write(f'   • Enrollments: {Enrollment.objects.count()}')
        self.stdout.write(f'   • Attendance Codes: {AttendanceCode.objects.count()}')
        self.stdout.write(f'   • Attendance Records: {AttendanceRecord.objects.count()}')
        
        try:
            justifications_final = AbsenceJustification.objects.count()
            self.stdout.write(f'   • Absence Justifications: {justifications_final}')
        except:
            self.stdout.write(f'   • Absence Justifications: N/A (model not available)')

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Database is now clean and ready for fresh data!'))
        self.stdout.write(f'👤 Login with: {admin_username} (password unchanged)')
        self.stdout.write(self.style.WARNING('\n💡 Run "python manage.py create_test_data" to populate with sample data'))