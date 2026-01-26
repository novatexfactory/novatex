import os
import tarfile
import datetime
import ftplib
import re
import logging
import subprocess

# Logging setup
logger = logging.getLogger('home')

def get_ftp_connection():
    host = os.getenv('ARVIXE_FTP_HOST')
    user = os.getenv('ARVIXE_FTP_USER')
    password = os.getenv('ARVIXE_FTP_PASSWORD')
    
    ftp = ftplib.FTP_TLS()
    ftp.connect(host, 21, timeout=60)
    ftp.auth()
    ftp.login(user, password)
    ftp.prot_p()
    return ftp

def transfer_with_verification(ftp, local_path):
    # Upload file
    with open(local_path, 'rb') as f:
        ftp.storbinary(f"STOR {local_path}", f)
    
    # Integrity check: compare sizes
    remote_size = ftp.size(local_path)
    local_size = os.path.getsize(local_path)
    
    if remote_size != local_size:
        raise Exception(f"Size mismatch for {local_path}: Local {local_size} vs Remote {remote_size}")
    return True

def run_backups():
    ftp = None
    date_str = datetime.datetime.now().strftime("%Y_%m_%d")
    
    # 1. Prepare Database Dump Credentials
    db_name = os.getenv('POSTGRES_DB', 'novatex_db')
    db_user = os.getenv('POSTGRES_USER', 'postgres')
    # Retrieve password to avoid interactive prompt
    db_password = os.getenv('SQL_PASSWORD') or os.getenv('POSTGRES_PASSWORD')
    db_file = f"db_backup_{date_str}.sql"
    
    # 2. Identify Log Files
    log_pattern = r'security\.log\.\d+'
    rotated_logs = [f for f in os.listdir('/app') if re.match(log_pattern, f)]
    log_archive = f"logs_backup_{date_str}.tar.gz"

    try:
        # Generate DB Dump
        # Prepare environment with PGPASSWORD to authenticate automatically
        env = os.environ.copy()
        if db_password:
            env['PGPASSWORD'] = db_password

        subprocess.run(
            ['pg_dump', '-h', 'db', '-U', db_user, '-f', db_file, db_name], 
            check=True, 
            env=env
        )
        
        # Create Log Archive
        if rotated_logs:
            with tarfile.open(log_archive, "w:gz") as tar:
                for log in rotated_logs:
                    tar.add(log)

        # Connect to Arvixe
        ftp = get_ftp_connection()

        # Transfer DB
        transfer_with_verification(ftp, db_file)
        os.remove(db_file)
        
        # Transfer Logs
        if rotated_logs and os.path.exists(log_archive):
            transfer_with_verification(ftp, log_archive)
            for log in rotated_logs:
                os.remove(log)
            os.remove(log_archive)

        logger.info("Backup process completed successfully.")

    except Exception as e:
        logger.error(f"Backup process failed: {str(e)}")
    
    finally:
        if ftp:
            try:
                ftp.quit()
            except:
                ftp.close()

if __name__ == "__main__":
    run_backups()