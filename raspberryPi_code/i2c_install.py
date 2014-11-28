import sys
import subprocess
import re
import fnmatch

def findReplace(filepath, find, replace):
	with open(filepath) as f:
		s = f.read()
		s = s.replace(find, replace)
	with open(filepath, "w") as f:
		f.write(s)
		f.close()

if len(sys.argv) < 2:
	print "Error: no arguments";
	sys.exit(1);

#------------------CHECK RASPBERRY PI SOFTWARE CONFIGURATION------------------
if (sys.argv[1]=="0") or (sys.argv[1]=="1"):
	# check if python-smbus package is installed
	cmd = "dpkg --status python-smbus"
	p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(output, err) = p.communicate();
	if output=="":
		print "ERROR: python-smbus not installed";
		if sys.argv[1]== "1":
			# INSTALL python-smbus
			cmd = "apt-get --yes --force-yes install python-smbus";
			p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			(output, err) = p.communicate();
			print output;
	else:
		print "python-smbus installed";

	# check if i2c-tools package is installed
	cmd = "dpkg --status i2c-tools"
	p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(output, err) = p.communicate();
	if output=="":
		print "ERROR: i2c-tools not installed";
		if sys.argv[1]== "1":
			# INSTALL python-smbus
			cmd = "apt-get --yes --force-yes install i2c-tools";
			p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			(output, err) = p.communicate();
			print output;
	else:
		print "i2c-tools installed";
	
	#read raspi-blacklist.conf file
	cmd = "cat /etc/modprobe.d/raspi-blacklist.conf"
	p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(output, err) = p.communicate();
	#check using regex if I2C is blacklisted in raspi-blacklist.conf
	i2cRegex = re.compile('[^#]blacklist i2c-bcm2708');
	i2cFindResult = i2cRegex.search(output);
	if i2cFindResult:
		print "ERORR: i2c is blacklisted"
		if sys.argv[1]== "1":
			findReplace("/etc/modprobe.d/raspi-blacklist.conf", "blacklist i2c-bcm2708","#blacklist i2c-bcm2708");
	else:
		print "i2c isn't blacklisted";
	#check using regex if SPI is blacklisted in raspi-blacklist.conf
	spiRegex = re.compile('[^#]blacklist spi-bcm2708');
	spiFindResult = spiRegex.search(output);
	if spiFindResult:
		print "ERORR: spi is blacklisted"
		if sys.argv[1]== "1":
			findReplace("/etc/modprobe.d/raspi-blacklist.conf", "blacklist spi-bcm2708","#blacklist spi-bcm2708");
	else:
		print "spi isn't blacklisted";
		
	#read /etc/modules file
	cmd = "cat /etc/modules"
	p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(output, err) = p.communicate();
	#check if i2c-dev module is load at boot time
	i2cRegex = re.compile("i2c-dev");
	i2cFindResult = i2cRegex.search(output);
	if i2cFindResult:
		print "i2c-dev module is enabled"
	else:
		print "ERROR: i2c-dev module is disabled in /etc/modules";
		if sys.argv[1]== "1":
			f = open('/etc/modules', 'a')
			f.write("\ni2c-dev")
			f.close()
	#check if snd-bcm2835 module is load at boot time
	i2cRegex = re.compile("snd-bcm2835");
	i2cFindResult = i2cRegex.search(output);
	if i2cFindResult:
		print "snd-bcm2835 module is enabled"
	else:
		print "ERROR: snd-bcm2835 module is disabled in /etc/modules";
		if sys.argv[1]== "1":
			f = open('/etc/modules', 'a')
			f.write("\nsnd-bcm2835")
			f.close()