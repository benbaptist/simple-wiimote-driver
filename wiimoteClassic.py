import struct, pymouse, pykeyboard, threading, time
### SETTINGS ###
MouseSensitivity = 0.6
### ACTUAL CODE - DON'T EDIT BELOW THIS UNLESS YOU KNOW WHAT YOU'RE DOING ###
f = open("/dev/input/js1", "r")
XPower = 0
YPower = 0
Hold = {}
k = pykeyboard.PyKeyboard()
m = pymouse.PyMouse()
def move(x, y):
	m.move(x, y)
def mouse():
	while True:
		print "bonk"
		if not XPower == 0 or not YPower == 0:
			x, y = m.position()
			print x, y, x + (XPower * MouseSensitivity), y + -(YPower * MouseSensitivity)
			try:
				move(x + (XPower * MouseSensitivity), y + -(YPower * MouseSensitivity))
			except:
				print "Error while m.move()"
				pass
		time.sleep(0.02)
t = threading.Thread(target=mouse, args=())
t.daemon = True
t.start()
buttons = {513: "X", 1: "A", 257: "B", 769: "Y", 
	1026: "Analog Right Trigger", 1281: "Right Trigger", 1282: "Analog Left Trigger", 1025: "Left Trigger",
	514: "Right Stick X-Axis", 770: "Right Stick Y-Axis", 2: "Left Stick X-Axis", 258: "Left Stick Y-Axis",
	1537: "ZL", 1793: "ZR", 2305: "Start", 2561: "Select", 2049: "Home"}
for i in buttons:
	Hold[buttons[i]] = 0
x, y = m.position()
def press(button):
	if button == "Start":
		k.press_key(k.escape_key)
	if button == "ZL":
		m.scroll(1)
	if button == "ZR":
		m.scroll(-1)
	if button == "Right Trigger":
		x, y = m.position()
		m.press(x, y, 1)
	if button == "Left Trigger":
		x, y = m.position()
		m.press(x, y, 3)
	if button == "B":
		k.press_key(" ")
def release(button):
	if button == "Start":
		k.release_key(k.escape_key)
	if button == "Right Trigger":
		x, y = m.position()
		m.release(x, y, 1)
	if button == "Left Trigger":
		x, y = m.position()
		m.release(x, y, 3)
	if button == "B":
		k.release_key(" ")
while True: # f.read(2).encode("hex")
	id = f.read(1).encode("hex")
	order = f.read(3).encode("hex")
	value = struct.unpack("h", f.read(2))[0]
	button = struct.unpack("h", f.read(2))[0]
	if button in buttons:
		name = buttons[button]
#		print buttons[button] + ": " + str(value)
		print name
		if name == "Right Stick X-Axis":
			XPower = value / 1000
			if XPower < 5 and XPower > -5: XPower = 0
		if name == "Right Stick Y-Axis":
			YPower = value / 1000
			if YPower < 5 and YPower > -5: YPower = 0
		if value == 1:
			press(name)
		else:
			release(name)
		Hold[name] = value
	else:
		print str(button) + ": " + str(value)
	if id == "c0c0": break
	 
#	length = f.read(4).encode("hex")
#	something = f.read(2)
#	thirty = f.read(2).encode("hex")
#	f.read(2 + 2 + 2 + 2 + 2 + 2)
#	print length, something, thirty
