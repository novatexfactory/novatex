import os
import subprocess
import datetime
import ftplib
import logging

logger = logging.getLogger('home')

def backup_database_to_arvixe():
    # 1. Данные из .env (те же, что мы проверили)
    host = os.getenv('ARVIXE_FTP_HOST')
    user = os.getenv('ARVIXE_FTP_USER')
    password = os.getenv('ARVIXE_FTP_PASSWORD')
    
    db_name = os.getenv('POSTGRES_DB', 'novatex_db')
    db_user = os.getenv('POSTGRES_USER', 'postgres')
    
    date_str = datetime.datetime.now().strftime("%Y_%m_%d")
    backup_file = f"db_backup_{date_str}.sql"
    ftp = None

    try:
        # 2. Создаем дамп базы внутри контейнера
        # Используем PGPASSWORD для автоматизации без запроса пароля
        env = os.environ.copy()
        result = subprocess.run(
            ['pg_dump', '-h', 'db', '-U', db_user, '-f', backup_file, db_name],
            env=env, capture_output=True, text=True
        )
        
        if result.returncode != 0:
            raise Exception(f"pg_dump error: {result.stderr}")

        # 3. Отправляем по FTPS
        ftp = ftplib.FTP_TLS()
        ftp.connect(host, 21, timeout=60)
        ftp.auth()
        ftp.login(user, password)
        ftp.prot_p()

        with open(backup_file, 'rb') as f:
            ftp.storbinary(f"STOR {backup_file}", f)
        
        # 4. Удаляем временный файл в AWS
        os.remove(backup_file)
        logger.info(f"Database backup successfully moved to Arvixe.")

    except Exception as e:
        logger.error(f"Database backup failed: {str(e)}")
    
    finally:
        if ftp:
            try: ftp.quit()
            except: ftp.close()

if __name__ == "__main__":
    backup_database_to_arvixe()