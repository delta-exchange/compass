import os
import paramiko
from scp import SCPClient
from src.util import logger

class SCPTransfer:
    @staticmethod
    def push_file_to_remote(local_file_path):
        logger.info(f"Pushing {local_file_path} to remote compass server")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        remote_host = os.getenv("COMPASS_HOST")
        username = os.getenv("COMPASS_USER")
        password = os.getenv("COMPASS_PASSWORD")
        ssh.connect(remote_host, username=username, password=password)

        scp = SCPClient(ssh.get_transport())
        scp.put(local_file_path, os.getenv("COMPASS_REPORTS_DIRECTORY"))
        scp.close()
        ssh.close()
        logger.info("File pushed to remote compass server")
