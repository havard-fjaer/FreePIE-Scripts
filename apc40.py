

MIDIDEVICE = 1
JOY_MIN = -17873
JOY_MAX = 17873


def readAxis():
	return filters.mapRange(midi[MIDIDEVICE].data.buffer[1], 0, 127, JOY_MIN, JOY_MAX)

def readButton():
	return midi[MIDIDEVICE].data.status == MidiStatus.NoteOn


def update():
	global povValue;
	
	# Global values
	channel = midi[MIDIDEVICE].data.channel
	buffer0 = midi[MIDIDEVICE].data.buffer[0]
	buffer1 = midi[MIDIDEVICE].data.buffer[1]
	status = midi[MIDIDEVICE].data.status
	
	# Diagnostics
	diagnostics.watch(channel)
	diagnostics.watch(buffer0)
	diagnostics.watch(buffer1)
	diagnostics.watch(status)
	diagnostics.watch(readButton())
	diagnostics.watch(readAxis())
	

	######################
	### vJoy Device #1 ###
	######################	

	### vJoy Device #1 - Sliders --> Axis ###
	if status == MidiStatus.Control and buffer0 == 7:
		
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
	
	### vJoy Device #1 - POV Hat Switch / BANK SELECT
	if (status == MidiStatus.NoteOn or status == MidiStatus.NoteOff) and channel == 0 and buffer0 >= 94 and buffer0 <= 97:
		
		if buffer0 == 94 and MidiStatus.NoteOn:
			povDirection = VJoyPov.Up
			
		if buffer0 == 95 and MidiStatus.NoteOn:
			povDirection = VJoyPov.Down
			
		if buffer0 == 96 and MidiStatus.NoteOn:
			povDirection = VJoyPov.Right
			
		if buffer0 == 97 and MidiStatus.NoteOn:
			povDirection = VJoyPov.Left
			
		if status == MidiStatus.NoteOff:
			povDirection = VJoyPov.Nil
			
		vJoy[0].setDigitalPov(0, povDirection)
	
	
	### vJoy Device #1 - Activator, Solo/Cue, Record arm --> Toggle buttons ###	
	if status == MidiStatus.NoteOn or status == MidiStatus.NoteOff:
		
		# Activator - Buttons 1-8(, 11-18, 21-28)
		for c in range(8): 
			if channel == c and buffer0 == 50:
				buttonIndex = c + 0
				vJoy[0].setButton(buttonIndex, readButton())	
	
		# Solo / Cue - Buttons 11-18
		for c in range(8): 
			if channel == c and buffer0 == 49:
				buttonIndex = c + 10
				vJoy[0].setButton(buttonIndex, readButton())	
	
		# Record Arm - Buttons 21-28
		for c in range(8): 
			if channel == c and buffer0 == 48:
				buttonIndex = c + 20
				vJoy[0].setButton(buttonIndex, readButton())	
	

	######################
	### vJoy Device #2 ###
	######################	
	
	### vJoy Device #2 - Track Control Sliders--> Axis ###	
	if status == MidiStatus.Control and channel == 0:
	
		# vJoy.1.x
		if buffer0 == 48:
			vJoy[1].x = readAxis()
	
		# vJoy.1.y
		if buffer0 == 49:
			vJoy[1].y = readAxis()
	
		# vJoy.1.z
		if buffer0 == 50:
			vJoy[1].z = readAxis()
	
		# vJoy.1.rx
		if buffer0 == 51:
			vJoy[1].rx = readAxis()
	
		# vJoy.1.ry
		if buffer0 == 52:
			vJoy[1].ry = readAxis()
	
		# vJoy.1.rz
		if buffer0 == 53:
			vJoy[1].rz = readAxis()
	
		# vJoy.1.slider
		if buffer0 == 54:
			vJoy[1].slider = readAxis()
	
		# vJoy.1.dial
		if buffer0 == 55:
			vJoy[1].dial = readAxis()			
			
	
	### vJoy Device #2 - Clip launch, Clip stop and Scene launch --> Momentary buttons ###
	if status == MidiStatus.NoteOn or status == MidiStatus.NoteOff:
		
		# Clip Launch - Buttons 1-8, 11-18, [...] through 48
		for c in range(8): # Channel
			for b in range(5): # Buffer0
				buttonMatrixY = b * 10 # Add 10 to each button row 
				buffer0Offset = 53 + b
				if channel == c and buffer0 == buffer0Offset:
					buttonIndex = buttonMatrixY + c # Add channel / column to row to get button index / number
					vJoy[1].setButton(buttonIndex, readButton())	
	
		# Scene Launch - Buttons 9, 19, 29, 39, 49
		for b in range(5):
			buttonMatrixY = (b * 10)
			buffer0Offset = 82 + b
			if channel == 0 and buffer0 == buffer0Offset:
				buttonIndex = buttonMatrixY + 8
				vJoy[1].setButton(buttonIndex, readButton())
	
		# Clip Stop - Buttons 51-58
		for c in range(8): 
			if channel == c and buffer0 == 52:
				buttonIndex = 50 + c
				vJoy[1].setButton(buttonIndex, readButton())	
		
		# Stop All Clips - Button 59 
		if channel == 0 and buffer0 == 81:
			vJoy[1].setButton(58, readButton())	

		# Track Control - Toggle buttons 61-64
		for b in range(4):
			buffer0Offset = 87 + b
			if channel == 0 and buffer0 == buffer0Offset:
				buttonIndex = b + 60
				vJoy[1].setButton(buttonIndex, readButton())

	######################
	### vJoy Device #3 ###
	######################
	
	# APC40 Device Control for Master Track - Channel 8. Device Control for Channel 0-7 is not mapped to any vJoy devices yet.
	if status == MidiStatus.Control and channel == 8:
	
		# vJoy.2.x
		if buffer0 == 16:
			vJoy[2].x = readAxis()
	
		# vJoy.2.y
		if buffer0 == 17:
			vJoy[2].y = readAxis()
	
		# vJoy.2.z
		if buffer0 == 18:
			vJoy[2].z = readAxis()
	
		# vJoy.2.rx
		if buffer0 == 19:
			vJoy[2].rx = readAxis()
	
		# vJoy.2.ry
		if buffer0 == 20:
			vJoy[2].ry = readAxis()
	
		# vJoy.2.rz
		if buffer0 == 21:
			vJoy[2].rz = readAxis()
	
		# vJoy.2.slider
		if buffer0 == 22:
			vJoy[2].slider = readAxis()
	
		# vJoy.2.dial
		if buffer0 == 23:
			vJoy[2].dial = readAxis()

	# Momentary buttons
	if status == MidiStatus.NoteOn or status == MidiStatus.NoteOff:

		# Track Control - Buttons 1-8
		for b in range(8):
			buffer0Offset = 58 + b
			if channel == 8 and buffer0 == buffer0Offset:
				vJoy[2].setButton(b, readButton())

	######################
	### vJoy Device #4 ###
	######################
	
	### vJoy Device #4 - Sliders --> Axis ###
	if status == MidiStatus.Control and channel == 0:
		
		# vJoy.3.x
		if buffer0 == 15:
			vJoy[3].x = readAxis()
	
		# vJoy.3.y
		if buffer0 == 14:
			vJoy[3].y = readAxis()

	### vJoy Device #4 - Buttons
	if (status == MidiStatus.NoteOn or status == MidiStatus.NoteOff) and channel == 0:
	
		# Playback, Bank select, Tempo, Misc - Buttons 1-11
		for b in range(11):
			buffer0Offset = 91 + b
			if buffer0 == buffer0Offset:
				vJoy[3].setButton(b, readButton())

	 
	 

	### vJoy Device #4 - Encoder - Cue Level
	if status == MidiStatus.Control and channel == 0 and buffer0 == 47:

		povMax = vJoy[3].continuousPovMax
		povIncrement = povMax / 100
		
		if buffer1 >= 120:
			vJoy[3].setPressed(11) # Encoder button down
			if povValue > 0:
				povValue -= povIncrement
			
		if buffer1 <= 10 :
			vJoy[3].setPressed(12) # Encoder button up
			if povValue < povMax:
				povValue += povIncrement
		
		vJoy[3].setAnalogPov(0, povValue)
			
			
		diagnostics.watch(vJoy[3].continuousPovMax)
		diagnostics.watch(povValue)
			


if starting:
	povValue = 0
	midi[MIDIDEVICE].update += update
	