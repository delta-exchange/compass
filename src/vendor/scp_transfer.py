import os
import paramiko
from scp import SCPClient
from src.util import logger

class SCPTransfer:
    @staticmethod
    def push_files_to_remote(local_folder):
        logger.info("Pushing files to remote compass server")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        remote_host = os.getenv("COMPASS_HOST")
        username = os.getenv("COMPASS_USER")
        password = os.getenv("COMPASS_PASSWORD")
        ssh.connect(remote_host, username=username, password=password)

        scp = SCPClient(ssh.get_transport())

        remote_folder = os.getenv("COMPASS_REPORTS_DIRECTORY")
        for filename in os.listdir(local_folder):
            logger.info(f"Pushing file {filename}")
            local_file = os.path.join(local_folder, filename)
            if os.path.isfile(local_file):
                remote_path = os.path.join(remote_folder, filename)
                scp.put(local_file, remote_path)

        scp.close()
        ssh.close()
        logger.info("Files pushed to remote compass server")
