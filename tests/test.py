# Import modules
import sys
#import paramiko

from PySide.QtCore import Qt
from PySide.QtGui import QApplication, QLabel
# Main 
if __name__ == '__main__':
	myApp = QApplication(sys.argv)
# Create all labels and set their properties
	appLabel = QLabel()
	appLabel.setText("Hello, World!!!\n lukasz_uszko 2014")
	appLabel.setAlignment(Qt.AlignCenter)
	appLabel.setWindowTitle("Uszko_Test_App")
	appLabel.setGeometry(300, 300, 300, 300)
	appLabel.show()
	 
 
	# hostname = "172:16:1:102"
	# password = "raspberry"
	# command = "ls"
 
	# username = "pi"
	# port = 22
 
	# try:
		# client = paramiko.SSHClient()
		# client.load_system_host_keys()
		# client.set_missing_host_key_policy(paramiko.WarningPolicy)
    
		# client.connect(hostname, port=port, username=username, password=password)
 
		# stdin, stdout, stderr = client.exec_command(command)
		# print stdout.read(),
 
	# finally:
		# client.close()
	# Execute the Application and Exit
	myApp.exec_()
	sys.exit()