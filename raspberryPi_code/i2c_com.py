import smbus
import sys
import threading
import math

I2Cbus = smbus.SMBus(1);

def readBlock(devAddr,startIndex,stopIndex):
	data=[]
	for i_read in range(0,int(stopIndex/32+1)):
		regBlock= I2Cbus.read_i2c_block_data(devAddr,0+i_read*32);
		data.extend(regBlock);
	return data[startIndex:stopIndex];
	#for i_read in range(startIndex,stopIndex):
	#	data.append(I2Cbus.read_word_data(devAddr,i_read));
	#return data;
	
def Test():
	registerValue=0;
	valueBit=0;
	bitmaskValue=0x01;
	mask=0x03;
	for i_bit in range(0,8):
		print(".");
		if (mask & (1<<i_bit))>0:
			#if(bitmaskValue&(1<<valueBit))>0:
			#	print ("*")
			#	registerValue=registerValue+(1<<i_bit);
			#valueBit=valueBit+1;
			registerValue=registerValue+(bitmaskValue<<i_bit)
			break;
	print (registerValue);
            

def setRegisters(devAddr,reg,value):
	I2Cbus.write_byte_data(devAddr,reg,value);
	
if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "Error: no arguments";
		sys.exit(1);

	if(sys.argv[1]=="read_block"):
		if len(sys.argv) < 4:
			print "Error: no arguments";
			sys.exit(1);
		devAddr = int(sys.argv[2],16);
		startIndex = int(sys.argv[3]);
		stopIndex = int(sys.argv[4]);
		print (readBlock(devAddr,startIndex,stopIndex));

	if(sys.argv[1]=="set_reg"):
		if len(sys.argv) < 4:
			print "Error: no arguments";
			sys.exit(1);
		devAddr = int(sys.argv[2],16);
		reg = int(sys.argv[3],16);
		value = int(sys.argv[4],16);
		setRegisters(devAddr,reg,value);
	
	if(sys.argv[1]=="test"):
		Test();