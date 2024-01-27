import subprocess


class SMB:

    def __init__(self, username, password, ip):
        self.username = username
        self.password = password
        self.ip = ip
    
    def connect(self):
        process = subprocess.Popen(
                [
                    "smbclient",
                    "-L",
                    "\\\\{}".format(self.ip),
                    "-U",
                    "{}%{}".format(self.username, self.password),
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout.decode('utf-8')


