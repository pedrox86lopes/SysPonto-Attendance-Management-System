# attendance/management/commands/populate_null_attendance_codes.py

from django.core.management.base import BaseCommand, CommandError
from attendance.models import AttendanceCode
from django.db import IntegrityError
import secrets
import string

class Command(BaseCommand):
    help = 'Populates NULL values in the AttendanceCode.code field with unique, randomly generated codes.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting to populate null attendance codes..."))

        codes_updated = 0
        qs_to_update = AttendanceCode.objects.filter(code__isnull=True)
        total_to_update = qs_to_update.count()

        if total_to_update == 0:
            self.stdout.write(self.style.SUCCESS("No null codes found. Exiting."))
            return

        for ac in qs_to_update:
            generated = False
            attempts = 0
            max_attempts = 100 # Prevent infinite loops in case of extreme collision

            while not generated and attempts < max_attempts:
                characters = string.ascii_uppercase + string.digits
                new_unique_code = ''.join(secrets.choice(characters) for _ in range(6))

                try:
                    # Check for existing code before trying to save
                    if not AttendanceCode.objects.filter(code=new_unique_code).exists():
                        ac.code = new_unique_code
                        ac.save(update_fields=['code'])
                        generated = True
                        codes_updated += 1
                    else:
                        self.stdout.write(self.style.WARNING(f"  Generated duplicate code {new_unique_code}, retrying... (Attempt {attempts + 1})"))
                except IntegrityError:
                    self.stdout.write(self.style.ERROR(f"  IntegrityError for code {new_unique_code}, retrying... (Attempt {attempts + 1})"))
                    pass # This should be rare if exists() check is effective
                attempts += 1
            
            if not generated:
                self.stdout.write(self.style.ERROR(f"  Failed to generate a unique code for AttendanceCode ID {ac.id} after {max_attempts} attempts. Skipping this record."))

        self.stdout.write(self.style.SUCCESS(f"Successfully updated {codes_updated} null codes out of {total_to_update} total."))
