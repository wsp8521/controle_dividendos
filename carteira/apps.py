import threading
from django.core.management import call_command
from django.apps import AppConfig
from django.core.management import CommandError

class CarteiraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carteira'

    def ready(self):
        import carteira.signals  # Garante que os signals sejam carregados


    #CÓDIGO TEMPORÁRIO. APÓS COLOCAR EM PRODUÇÃO REMOVER ESSE CÓDGIO E UTILZIAR O CRON JOB N0 SERVIDOR
        # Evita múltiplas execuções
        if not hasattr(self, 'run_once'):
            self.run_once = True
            threading.Thread(target=self.run_command, daemon=True).start()

    def run_command(self):
        """Executa o comando em uma thread separada para não travar o Django."""
        try:
            call_command("atualizar_status")
            print("✅ Status atualizado com sucesso!")
        except CommandError as e:
            print(f"❌ Erro ao atualizar status: {e}")
        except Exception as e:
            print(f"⚠️ Erro inesperado: {e}")
