#uszko 22-11-2014
import paramiko, base64
import time
import select 
import sys



class SshConnection:
    def __init__(self,hostname,port,username,password):
        self.hostname = hostname
        self.username = username
        self.password = password 
        self.command =''
        self.port = 22
        self.sshClient=None
        #jakbys my z jakimis kluczami 
        # if key is not None:
             # key = paramiko.RSAKey.from_private_key(StringIO(key), password=passphrase)
             # self.client.connect(host, port, username=username, password=password, pkey=key, timeout=self.TIMEOUT)
        # hostname = '172.16.1.102'
        # password = 'raspberry'
        # command = 'ls'
        # username = 'pi'
        # port = 22

    def connect(self):
        # Try to connect to the host.
        # Retry a few times if it fails.
        nrOfTries =10
        i = 1
        while True:
            print ("Trying to connect to %s (%i/%i)" % (self.hostname, i,nrOfTries))
            try:
                self.sshClient = paramiko.SSHClient()
                self.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.sshClient.connect(self.hostname, port=self.port, username=self.username, password=self.password)
                print ("Connected to %s" % self.hostname)
                break
            except paramiko.AuthenticationException:
                print ("Authentication failed when connecting to %s" % self.hostname)
                sys.exit(1)
            except:
                print ("Could not SSH to %s, waiting for it to start" % self.hostname)
                i += 1
                if i==nrOfTries:
                    break
                time.sleep(1)
        stdin, stdout, stderr = self.sshClient.exec_command('ls')
        for line in stdout:
            print (line.strip('\n'))

    def close(self):
        if self.sshClient is not None:
           self.sshClient.close()
           self.sshClient = None
    
    def executeCommand(self, command):
        stdin, stdout, stderr = self.sshClient.exec_command(command)
        return {'STDOUT': stdout.readlines(), 
                'STDERR': stderr.readlines(),
                'RET_VAL': stdout.channel.recv_exit_status()}

#DEBUG
if __name__ == "__main__":
    client = SshConnection('192.168.1.13', 22, 'pi', 'raspberry') 
    try:
      client.connect()
    finally:
      client.close() 
