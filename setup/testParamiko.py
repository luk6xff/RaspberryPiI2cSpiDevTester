import paramiko, base64
import time
import select 
import sys
hostname = '172.16.1.102'
password = 'raspberry'
command = 'ls'
 
username = 'pi'
port = 22



# def test_ssh(host, username, password):
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect(host, username=username, password=password)

# test_ssh(hostname, username, password)	
i = 1

#
# Try to connect to the host.
# Retry a few times if it fails.
#
while True:
    print ("Trying to connect to %s (%i/30)" % (hostname, i))

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)
        print ("Connected to %s" % hostname)
        break
    except paramiko.AuthenticationException:
        print ("Authentication failed when connecting to %s" % hostname)
        sys.exit(1)
    except:
        print ("Could not SSH to %s, waiting for it to start" % hostname)
        i += 1
        time.sleep(2)
stdin, stdout, stderr = client.exec_command('ls')
for line in stdout:
    print (line.strip('\n'))
stdin, stdout, stderr = client.exec_command('sudo su')
# time.sleep(2)
# for line in stdout:
    # print (line.strip('\n'))
channel = client.get_transport().open_session()
channel.exec_command('python SI7020Test.py')                      
#channel.exec_command("/tmp/test.sh")  
#stdin, stdout, stderr = client.exec_command('python SI7020Test.py')
# Wait for the command to terminate
while not stdout.channel.exit_status_ready():
	time.sleep(2)
	# for line in stdout:
		# print (line.strip('\n'))
	#if channel.exit_status_ready():                                
           # break
		   # Only print data if there is data to read in the channel
	#if (stdout.channel.recv_ready()):
	r, w, x = select.select([channel], [], [])
	if len(r) > 0:                                                 
		print (channel.recv(1024)) 
	#print (stdout.printlines())		
#
# Disconnect from the host
#
print ("Command done, closing SSH connection")
client.close()




# import sys, paramiko
 
 
# hostname = '172:16:1:102'
# password = 'raspberry'
# command = 'ls'
 
# username = 'pi'
# port = 22
 
# try:
    # client = paramiko.SSHClient()
    # client.load_system_host_keys()
    # client.set_missing_host_key_policy(paramiko.WarningPolicy)
    
    # client.connect(hostname, port=port, username=username, password=password)
 
    # stdin, stdout, stderr = client.exec_command(command)
    # sys.stdout.read()
 
# finally:
    # client.close()
	
	
	
	
# #from StringIO import StringIO
# import paramiko 

# class SshClient:
    # "A wrapper of paramiko.SSHClient"
    # TIMEOUT = 4

    # def __init__(self, host, port, username, password, key=None, passphrase=None):
        # self.username = username
        # self.password = password
        # self.client = paramiko.SSHClient()
        # self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # if key is not None:
            # key = paramiko.RSAKey.from_private_key(StringIO(key), password=passphrase)
        # self.client.connect(host, port, username=username, password=password, pkey=key, timeout=self.TIMEOUT)

    # def close(self):
        # if self.client is not None:
            # self.client.close()
            # self.client = None

    # def execute(self, command, sudo=False):
        # feed_password = False
        # if sudo and self.username != "root":
            # command = "sudo -S -p '' %s" % command
            # feed_password = self.password is not None and len(self.password) > 0
        # stdin, stdout, stderr = self.client.exec_command(command)
        # if feed_password:
            # stdin.write(self.password + "\n")
            # stdin.flush()
        # return {'out': stdout.readlines(), 
                # 'err': stderr.readlines(),
                # 'retval': stdout.channel.recv_exit_status()}

# if __name__ == "__main__":
    # client = SshClient(host='172:16:1:102', port=22, username='pi', password='raspberry') 
    # try:
       # ret = client.execute('dmesg', sudo=True)
       # print (''.join(ret["out"]), "  E ".join(ret["err"]), ret["retval"])
    # finally:
      # client.close() 
	
	