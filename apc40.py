

MIDIDEVICE = 1
JOY_MIN = -17873
JOY_MAX = 17873

def readAxis():
	return filters.mapRange(midi[MIDIDEVICE].data.buffer[1], 0, 127, JOY_MIN, JOY_MAX)


def update():
	channel = midi[MIDIDEVICE].data.channel
	buffer0 = midi[MIDIDEVICE].data.buffer[0]
	buffer1 = midi[MIDIDEVICE].data.buffer[1]
	status = midi[MIDIDEVICE].data.status
	
	diagnostics.watch(channel)
	diagnostics.watch(buffer0)
	diagnostics.watch(buffer1)
	diagnostics.watch(status)
	
	channel = midi[MIDIDEVICE].data.channel
	buffer0 = midi[MIDIDEVICE].data.buffer[0]

	######################
	### vJoy Device #1 ###
	######################	

	### vJoy Device #1 - Sliders --> Axis ###
	
	# vJoy.0.x
	if channel == 0 and buffer0 == 7:
		vJoy[0].x = readAxis()

	# vJoy.0.y
	if channel == 1 and buffer0 == 7:
		vJoy[0].y = readAxis()

	# vJoy.0.z
	if channel == 2 and buffer0 == 7:
		vJoy[0].z = readAxis()

	# vJoy.0.rx
	if channel == 3 and buffer0 == 7:
		vJoy[0].rx = readAxis()

	# vJoy.0.ry
	if channel == 4 and buffer0 == 7:
		vJoy[0].ry = readAxis()

	# vJoy.0.rz
	if channel == 5 and buffer0 == 7:
		vJoy[0].rz = readAxis()

	# vJoy.0.slider
	if channel == 6 and buffer0 == 7:
		vJoy[0].slider = readAxis()

	# vJoy.0.dial
	if channel == 7 and buffer0 == 7:
		vJoy[0].dial = readAxis()
	
	### vJoy Device #1 - Activator, Solo/Cue, Record arm --> Toggle buttons ###	
	# TODO
	

	######################
	### vJoy Device #2 ###
	######################
	
	
	### vJoy Device #2 - Track Control Sliders--> Axis ###
	
	# vJoy.1.x
	if channel == 0 and buffer0 == 48:
		vJoy[1].x = readAxis()

	# vJoy.1.y
	if channel == 0 and buffer0 == 49:
		vJoy[1].y = readAxis()

	# vJoy.1.z
	if channel == 0 and buffer0 == 50:
		vJoy[1].z = readAxis()

	# vJoy.1.rx
	if channel == 0 and buffer0 == 51:
		vJoy[1].rx = readAxis()

	# vJoy.1.ry
	if channel == 0 and buffer0 == 52:
		vJoy[1].ry = readAxis()

	# vJoy.1.rz
	if channel == 0 and buffer0 == 53:
		vJoy[1].rz = readAxis()

	# vJoy.1.slider
	if channel == 0 and buffer0 == 54:
		vJoy[1].slider = readAxis()

	# vJoy.1.dial
	if channel == 0 and buffer0 == 55:
		vJoy[1].dial = readAxis()
		
	### vJoy Device #2 - Track Control Buttons --> Toggle buttons ###	
	# TODO
	
	### vJoy Device #2 - Clip launch, Clip stop and Scene launch --> Momentary buttons ###
	# TODO


	### vJoy Device #3 ###
	# APC40: Master Device - Channel 8 
	
	# vJoy.2.x
	if channel == 8 and buffer0 == 16:
		vJoy[2].x = readAxis()

	# vJoy.2.y
	if channel == 8 and buffer0 == 17:
		vJoy[2].y = readAxis()

	# vJoy.2.z
	if channel == 8 and buffer0 == 18:
		vJoy[2].z = readAxis()

	# vJoy.2.rx
	if channel == 8 and buffer0 == 19:
		vJoy[2].rx = readAxis()

	# vJoy.2.ry
	if channel == 8 and buffer0 == 20:
		vJoy[2].ry = readAxis()

	# vJoy.2.rz
	if channel == 8 and buffer0 == 21:
		vJoy[2].rz = readAxis()

	# vJoy.2.slider
	if channel == 8 and buffer0 == 22:
		vJoy[2].slider = readAxis()

	# vJoy.2.dial
	if channel == 8 and buffer0 == 23:
		vJoy[2].dial = readAxis()
		
	


if starting:
	midi[MIDIDEVICE].update += update