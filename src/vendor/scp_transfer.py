import os
import paramiko
from scp import SCPClient
from src.util import logger, DateTimeUtil

class SCPTransfer:
    @staticmethod
    def push_files_to_remote_server_by_directory(directory, eod_file_path = f"EOD{DateTimeUtil.get_current_date()}.csv"):
        logger.info(f"Pushing files to remote compass server from {directory}")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        remote_host = os.getenv("COMPASS_HOST")
        username = os.getenv("COMPASS_USER")
        password = os.getenv("COMPASS_PASSWORD")
        ssh.connect(remote_host, username=username, password=password)

        scp = SCPClient(ssh.get_transport())
        for file in os.listdir(directory):
            logger.info(f"Pushing file {file} to remote compass server")
            scp.put(os.path.join(directory, file), os.getenv("COMPASS_REPORTS_DIRECTORY"))
        scp.close()

        logger.info(f"Pushing EOD file {eod_file_path} to remote compass server")
        scp = SCPClient(ssh.get_transport())
        scp.put(os.path.join(directory, eod_file_path), os.getenv("COMPASS_REPORTS_DIRECTORY"))
        scp.close()
        ssh.close()
        logger.info("Files pushed to remote compass server")