import ssl
from django.core.mail.backends.smtp import EmailBackend

class ArvixeEmailBackend(EmailBackend):
    """
    Кастомный бэкенд для обхода проблем с самоподписанными 
    сертификатами на серверах Arvixe.
    """
    def open(self):
        if self.connection:
            return False
        try:
            # Принудительно используем незащищенный контекст
            context = ssl._create_unverified_context()
            self.connection = self.connection_class(
                self.host, self.port, timeout=self.timeout, context=context
            )
            self.connection.login(self.username, self.password)
            return True
        except Exception:
            if not self.fail_silently:
                raise
            return False