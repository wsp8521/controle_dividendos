from django.apps import AppConfig
from django.core.management import call_command
import threading

class CarteiraConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'carteira'

  #habilitando signals na aplicação
  def ready(self):
      import carteira.signals
      """Executa o comando atualizar_status quando o Django inicia."""
      if not hasattr(self, 'run_once'):
          self.run_once = True
          threading.Thread(target=self.run_command).start()

  #atualzia o status dos proventos
  def run_command(self):
      """Executa o comando em uma thread separada para não travar o Django."""
      try:
          call_command("atualizar_status")
          print("✅ Status atualizado com sucesso!")
      except Exception as e:
          print(f"❌ Erro ao atualizar status: {e}")
