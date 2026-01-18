import os
import tarfile
import datetime
import ftplib
import re
import logging

logger = logging.getLogger('home')

def archive_and_move_to_arvixe():
    host = os.getenv('ARVIXE_FTP_HOST')
    user = os.getenv('ARVIXE_FTP_USER')
    password = os.getenv('ARVIXE_FTP_PASSWORD')

    log_files = [f for f in os.listdir('/app') if re.match(r'security\.log\.\d+', f)]
    if not log_files:
        return

    archive_name = f"novatex_logs_{datetime.datetime.now().strftime('%Y_%m_%d')}.tar.gz"
    ftp = None  # Инициализируем переменную для блока finally

    try:
        # 1. Создаем архив
        with tarfile.open(archive_name, "w:gz") as tar:
            for file in log_files:
                tar.add(file)

        # 2. Настраиваем соединение
        ftp = ftplib.FTP_TLS()
        ftp.connect(host, 21, timeout=30)
        ftp.auth()
        ftp.login(user, password)
        ftp.prot_p()

        # 3. Передача файла
        with open(archive_name, 'rb') as f:
            ftp.storbinary(f"STOR {archive_name}", f)

        # 4. Удаление оригиналов (только если передача прошла успешно)
        for file in log_files:
            os.remove(os.path.join('/app', file))
        os.remove(archive_name)
        
        logger.info(f"Successfully archived and moved logs to Arvixe.")

    except Exception as e:
        logger.error(f"Critical error during log transfer: {str(e)}")
    
    finally:
        # 5. ГАРАНТИРОВАННОЕ закрытие соединения
        if ftp:
            try:
                ftp.quit() # Пытаемся выйти вежливо
            except:
                ftp.close() # Если вежливо не вышло (обрыв связи), закрываем сокет принудительно