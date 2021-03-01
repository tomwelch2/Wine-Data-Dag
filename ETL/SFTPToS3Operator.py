import paramiko
import boto3
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

class SFTPToS3Operator(BaseOperator):
    @apply_defaults
    def __init__(
                self,
                aws_access_key_id: str,
                aws_secret_access_key: str,
                region_name: str,
                bucket_name: str,
                pkey: str,
                ip: str,
                username: str,
                file_to_download: str,
                save_as: str,
                **kwargs
                )->None:
        super().__init__(**kwargs)
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.bucket_name = bucket_name
        self.pkey = pkey,
        self.ip = ip
        self.username = username
        self.file_to_download = file_to_download
        self.save_as = save_as

    def execute(self, context):
        ssh = paramiko.SSHClient()
        key = paramiko.RSAKey.from_private_key_file(self.pkey)
        ssh.get_host_keys().add(self.ip, "ssh-rsa", key)
        ssh.load_system_host_keys()
        ssh.connect(self.ip, username = self.username, pkey = key)
        transfer = ssh.open_sftp()
        transfer.get(self.file_to_download, self.local_file_path)

        S3 = boto3.client(
                    service_name = "s3",
                    aws_access_key_id = self.aws_access_key_id,
                    aws_secret_access_key = self.aws_secret_access_key,
                    region_name = self.region_name
                )

        with open(self.local_file_path, "rb") as f:
            S3.upload_fileobj(f, self.bucket_name, self.save_as)



