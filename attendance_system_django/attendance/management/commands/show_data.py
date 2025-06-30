from django.core.management.base import BaseCommand
from attendance.models import AttendanceRecord, AttendanceCode

class Command(BaseCommand):
    help = 'Mostra dados capturados de forma organizada'

    def handle(self, *args, **options):
        self.stdout.write("=== DADOS DE PRESENÇA ===")
        
        # Estatísticas gerais
        total = AttendanceRecord.objects.count()
        approved = AttendanceRecord.objects.filter(is_present=True).count()
        
        self.stdout.write(f"Total submissões: {total}")
        self.stdout.write(f"Aprovadas: {approved}")
        self.stdout.write(f"Taxa aprovação: {(approved/total*100):.1f}%" if total > 0 else "0%")
        
        # Últimas 10 submissões
        self.stdout.write("\n=== ÚLTIMAS SUBMISSÕES ===")
        recent = AttendanceRecord.objects.select_related('student').order_by('-timestamp')[:10]
        
        for record in recent:
            ai_status = "Suspeita" if record.ai_result and record.ai_result.get('isFraudulent') else "🟢 OK"
            approval = "Aprovada" if record.is_present else "⏳ Pendente"
            
            self.stdout.write(
                f"{record.student.username:<15} | "
                f"{record.timestamp.strftime('%d/%m/%Y, %H:%M:%S'):<12} | "
                f"{ai_status:<10} | "
                f"{approval}"
            )
            
            