import time
import socket
import pyautogui
import time
import threading

pyautogui.PAUSE = 0.01
button ='$'
duty_ratio = 0


class myThread (threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):
		while(True):
			if(button!='$'):
				pyautogui.keyDown(button)
				time.sleep((0.15/(25))*duty_ratio)
				time.sleep((0.15/(25))*(1-duty_ratio))
				pyautogui.keyUp(button)

thread1 = myThread(1, "Thread-1", 1)

def main():
	s = socket.socket()
	thread1.start()
	print("Socket successfully created.")

	while True:
		try:
			print("enter port (leave blank for 4444): ",end="")
			inp = input()

			if inp == '':
				port = 4444
			else:
				port = int(inp)

			s.bind(('', port))
			print ("socket binded to %s" %(port))
			break
		except OSError:
			print("Port " + str(port) + " is already in use. Please use the following command:")
			print("lsof -n -i4TCP:4444 | grep LISTEN")
			exit()
		except:
			print ("unexpected error while connecting to port")

	s.listen()
	print ("socket is listening...")
	while True:

		c, addr = s.accept()

		print ('Got connection from', addr)

		while True:
			message = c.recv(256).decode("utf-8"); #message comes in byte array so change it to string first
			message = message.split("%") #use & to split tokens, and % to split messages.
			for msg in message:
				msg = msg.split("&")
				print("DEBUG: ",msg)
				if(msg[0] == 'wasd'):
    					wasd(msg[1], msg[2])
				elif(msg[0]=='tilt'):
					if(len(msg)==2):
						if(msg[1]=='0'):
							global button
							button='$'
					if(len(msg)<3):
						continue
					elif(msg[2]==''):
						continue
					elif msg[1]=='+':
						tilt(True,float(msg[2]))
					elif msg[1]=='-':
						tilt(False,float(msg[2]))
			c.send(bytes('Thank you for connecting', "utf-8"))
		c.close()

def wasd(type, msg):
	if(type == 'down'):
		pyautogui.keyDown(msg)
	else:
		pyautogui.keyUp(msg)

def press(duty_ratio,button):
	j = 15
	for i in range (j-6):
		pyautogui.keyDown(button)
		time.sleep((0.15/(j))*duty_ratio)
		pyautogui.keyUp(button)


def tilt(message,value):
	global button
	if message:
		button = 'a'
		duty_ratio = value/14
	else:
		button = 'd'
		duty_ratio = value/14

if __name__=="__main__":
	main()
