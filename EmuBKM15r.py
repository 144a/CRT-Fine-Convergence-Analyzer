import socket
#import keyboard
import time

#HOST = "127.0.0.1"  # The server's hostname or IP address
#PORT = 65432  # The port used by the server

HOST = "192.168.0.1"
PORT = 53484


# Beginning header for All commands
# 0x30, 0x0B, 'S', 'O', 'N', 'Y', 0x00, 0x00, 0x0B, 0x00, 0x00
header = bytes.fromhex("030B534F4E59000000B00000")

# General Status Request from remote
status = bytes.fromhex("030B534F4E59000000B0000012535441546765742043555252454E54203500")

def displayCommands():
	print("List of Supported Commands:")
	print("#-----Menu Control Commands-----#")
	print("'MenuEnt' - Ent at numeric keys")
	print("'MenuDel' - Del at numeric keys")
	print("'Menu' - Menu")
	print("'Enter' - Menu Enter")
	print("'Up' - Up")
	print("'Down' - Down")
	print("'0' through '9' - Number Pad Inputs (Single Digits)")
	print("")
	print("#-----Modification Commands-----#")
	print("'Power' - Power")
	print("'Degauss' - Degauss")
	print("'ScanMode' - Scanmode (Underscan)")
	print("'HorizDelay' - Horizontal delay")
	print("'VertDelay' - Vertical delay")
	print("'Mono' - Monochrome")
	print("'Aperture' - Aperture")
	print("'Comb' - Comb")
	print("'CharMute' - Char Off")
	print("'ColorTemp' - Color Temp.")
	print("'Aspect' - Aspect ratio (16:9)")
	print("'ExtSync' - External sync")
	print("'BlueOnly' - Blue only")
	print("'RedCut' - R Cutoff")
	print("'GreenCut' - G Cutoff")
	print("'BlueCut' - B Cutoff")
	print("'Marker' - Marker mode")
	print("'ChromaUp' - Chroma up")
	print("")

def getCommand(m, s):
	# Status Command
	ret = b'\x00'

	if(m == "Status"):
		return status


	# --- Navigation Commands --- #

	# Menu Command
	if(m == "Menu"):
		ret = str.encode("INFObutton MENU ")
	# Enter Command
	if(m == "Enter"):
		ret = str.encode("INFObutton MENUENT ")


	# Up Command
	if(m == "Up"):
		ret = str.encode("INFObutton MENUUP ")
	# DownCommand
	if(m == "Down"):
		ret = str.encode("INFObutton MENUDOWN ")

	# Numberpad Enter
	if(m == "Ent"):
		ret = str.encode("INFObutton ENTER ")
	# Numberpad Delete
	if(m == "Del"):
		ret = str.encode("INFObutton DELETE ")

	# Number 0
	if(m == "0"):
		ret = str.encode("INFObutton 0 ")
	# Number 1
	if(m == "1"):
		ret = str.encode("INFObutton 1 ")
	# Number 2
	if(m == "2"):
		ret = str.encode("INFObutton 2 ")
	# Number 3
	if(m == "3"):
		ret = str.encode("INFObutton 3 ")
	# Number 4
	if(m == "4"):
		ret = str.encode("INFObutton 4 ")
	# Number 5
	if(m == "5"):
		ret = str.encode("INFObutton 5 ")
	# Number 6
	if(m == "6"):
		ret = str.encode("INFObutton 6 ")
	# Number 7
	if(m == "7"):
		ret = str.encode("INFObutton 7 ")
	# Number 8
	if(m == "8"):
		ret = str.encode("INFObutton 8 ")
	# Number 9
	if(m == "9"):
		ret = str.encode("INFObutton 9 ")


	# --- Modification Command --- #

	# Power Command
	if(m == "Power"):
		ret = str.encode("STATset POWER TOGGLE")

	# Degauss Command
	if(m == "Degauss"):
		ret = str.encode("STATset DEGAUSS TOGGLE")

	if(m == "ScanMode"):
		ret = str.encode("STATset SCANMODE TOGGLE")
	if(m == "HorizDelay"):
		ret = str.encode("STATset HDELAY TOGGLE")
	if(m == "VertDelay"):
		ret = str.encode("STATset VDELAY TOGGLE")
	if(m == "Mono"):
		ret = str.encode("STATset MONOCHR TOGGLE")
	if(m == "Comb"):
		ret = str.encode("STATset COMB TOGGLE")
	if(m == "CharMute"):
		ret = str.encode("STATset CHARMUTE TOGGLE")
	if(m == "ColorTemp"):
		ret = str.encode("STATset COLADJ TOGGLE")
	if(m == "Aspect"):
		ret = str.encode("STATset ASPECT TOGGLE")
	if(m == "ExtSync"):
		ret = str.encode("STATset EXTSYNC TOGGLE")
	if(m == "BlueOnly"):
		ret = str.encode("STATset BLUEONLY TOGGLE")
	if(m == "RedCut"):
		ret = str.encode("STATset RCUTOFF TOGGLE")
	if(m == "BlueCut"):
		ret = str.encode("STATset BCUTOFF TOGGLE")
	if(m == "GreenCut"):
		ret = str.encode("STATset GCUTOFF TOGGLE")
	if(m == "Marker"):
		ret = str.encode("STATset Marker TOGGLE")
	if(m == "ChromaUp"):
		ret = str.encode("STATset CHROMAUP TOGGLE")

	# Knobs
	if(m.find("PhaseInc") > -1):
		ret = str.encode("INFOknob R PHASE 96/" + str(m[m.find(" ")+1:]) + "/21")
	if(m.find("ChromaInc") > -1):
		ret = str.encode("INFOknob R CHROMA 96/" + str(m[m.find(" ")+1:]) + "/21")
	if(m.find("BrightnessInc") > -1):
		ret = str.encode("INFOknob R BRIGHTNESS 96/" + str(m[m.find(" ")+1:]) + "/21")
	if(m.find("ContrastInc") > -1):
		ret = str.encode("INFOknob R CONTRAST 96/" + str(m[m.find(" ")+1:]) + "/21")
	if(m.find("PhaseDec") > -1):
		ret = str.encode("INFOknob R PHASE 96/-" + str(m[m.find(" ")+1:]) + "/21")
	if(m.find("ChromaDec") > -1):
		ret = str.encode("INFOknob R CHROMA 96/-" + str(m[m.find(" ")+1:]) + "/21")
	if(m.find("BrightnessDec") > -1):
		ret = str.encode("INFOknob R BRIGHTNESS 96/-" + str(m[m.find(" ")+1:]) + "/21")
	if(m.find("ContrastDec") > -1):
		ret = str.encode("INFOknob R CONTRAST 96/-" + str(m[m.find(" ")+1:]) + "/21")

	if ret == b'\x00':
		print("Warning, not a recognized command. Might have unexpected effects.")
		return

	# Return properly formatted command (header + payload length + payload)
	com = header + (len(ret)).to_bytes(1, 'big') + ret

	# Send Command
	s.send(com)
	data = s.recv(1024)
	if data == b'\x03\x0bSONY\x00\x00\x01\xb0\x00\x00\x00':
		print("Command Recieved Successfully")

def connect_to_monitor():
	print("EmuBKM-15R: A simple script to emulate the Sony BKM-15R Controllers for A series Sony BVMs")
	print("Written by 144a aka Andy Gatza")
	print("Credit for Reverse Engineering goes to Martin Hejnfelt")
	print("")
	print("")
	print("")
	print("Connecting...")
	print("")

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	print("Connected!")

	return s


if __name__ == '__main__':
	s = connect_to_monitor()

	print("If you need help, run the 'help' command!")
	print("")
	print("")

	inp = ""
	while(inp != "exit"):
		inp = input(">")
		if inp == "help":
			displayCommands()

		elif inp == "ChannelName":
			getCommand("Menu", s)
			getCommand("Down", s)
			getCommand("Down", s)
			getCommand("Enter", s)
			channel = input("What Channel would you like to rename? ")
			if channel.isnumeric() and int(channel) >= 0 and int(channel) < 98:
				if len(channel) == 1:
					getCommand(channel, s)
				else:
					getCommand("0", s)
					getCommand(channel[0], s)
					getCommand(channel[1], s)

				getCommand("Up", s)
				getCommand("Down", s)
				getCommand("Down", s)
				getCommand("Down", s)
				getCommand("Enter", s)
				getCommand("Up", s)
				getCommand("Enter", s)

				charset = "%abcdefghijklmnopqrstuvwxyz0123456789(,):;.-+/&"

				isgood = False
				while isgood == False:
					name = input("What would you like to name the channel? ").lower()
					if len(name) > 20:
						print("Channel name too long")
					elif len(name) == 0:
						print("No name Entered")
					else:
						isgood = True

				for t in name:
					dir = 1
					count = charset.index(t)
					if count > len(charset) // 2:
						dir = -1
						count = len(charset) - count + 1

					for i in range(count):
						if dir == 1:
							getCommand("Up", s)
						else:
							getCommand("Down", s)
						time.sleep(0.02)
					time.sleep(0.02)
					getCommand("Enter", s)

				getCommand("Enter", s)
				print("Updated Channel Name Successfully!")
			else:
				print("Error: Not a valid channel")

		elif inp != "exit":
			getCommand(inp, s)
		else:
			print("Unknown Command")


	#	if keyboard.read_key() == "p":
	#		print("Requesting Status:")
	#		s.send(powerc)
	#		data = s.recv(1024)
	#		print(f"Received {data!r}")

	#	if keyboard.read_key() == "q":
	#		print("Exiting...")
	#		break


	print("Exited Successfully")

