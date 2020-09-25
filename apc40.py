from array import *
import time

MIDIDEVICE = 1
JOY_MIN = -17873
JOY_MAX = 17873
JOY_DEV_0 = 0
JOY_DEV_1 = 1
JOY_DEV_2 = 2
JOY_DEV_3 = 3

class MidiEncoder:
	def __init__(self, vJoyDev, buttonOffset):
		self.previousRawMidiValue = 0
		self.vJoyDev = vJoyDev
		self.buttonState = False
		self.buttonOffset = buttonOffset
		self.downButton = self.buttonOffset
		self.upButton = self.buttonOffset + 1
		self.currentDirection = 0
		self.previousDirection = 0
		self.ticksSinceLastDirectionUpdate = 0
		self.buttonActivatedClock = time.clock()
		self.offButtonDelay = 0.05
		self.updateEncoderTickInterval = 10 # Update soft encoder every 10 ticks from raw MIDI encoder
	
	
	def checkButtonOffDelay(self): 
		if self.buttonActivatedClock + self.offButtonDelay < time.clock():
			self.buttonState = False
			vJoy[self.vJoyDev].setButton(self.downButton, 0)
			vJoy[self.vJoyDev].setButton(self.upButton, 0)
					
	
	def updateEncoderButtonState(self, currentRawMidiValue):
		
		direction = self.getUpdatedDirection(currentRawMidiValue)
		
		if direction == -1:
			vJoy[self.vJoyDev].setButton(self.downButton, 1)
			self.buttonState = True
			self.buttonActivatedClock = time.clock()
		
		if direction == 1:
			vJoy[self.vJoyDev].setButton(self.upButton, 1)
			self.buttonState = True
			self.buttonActivatedClock = time.clock()
	
	
	def getUpdatedDirection(self, currentRawMidiValue):
		
		exposedDirection = 0 
		
		if currentRawMidiValue > self.previousRawMidiValue or currentRawMidiValue == 127:
			self.currentDirection = 1
			
		if currentRawMidiValue < self.previousRawMidiValue or currentRawMidiValue == 0:
			self.currentDirection = -1
		
		# Direction change
		if self.currentDirection != self.previousDirection:			
			self.previousDirection = self.currentDirection			
			self.ticksSinceLastDirectionUpdate = 0 
			# Expose direction change, regardless of counter
			exposedDirection = self.currentDirection 
		
		# Expose current direction if ticks has passed configured interval
		if self.ticksSinceLastDirectionUpdate >= self.updateEncoderTickInterval:
			exposedDirection = self.currentDirection
			self.ticksSinceLastDirectionUpdate = 0
		
		self.previousRawMidiValue = currentRawMidiValue
		self.ticksSinceLastDirectionUpdate += 1

		return exposedDirection
			

def readAxis():
	return filters.mapRange(midi[MIDIDEVICE].data.buffer[1], 0, 127, JOY_MIN, JOY_MAX)

def readEncoder():
	return midi[MIDIDEVICE].data.buffer[1]

def readButton():
	return midi[MIDIDEVICE].data.status == MidiStatus.NoteOn

def update():
	global povValue
	global encoders
	global lastButtonPressed
	global timepress
	
	# MIDI
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

	# Axis - from Track sliders 
	if status == MidiStatus.Control and buffer0 == 7:
		
		# x
		if channel == 0 and buffer0 == 7:
			vJoy[JOY_DEV_0].x = readAxis()
	
		# y
		if channel == 1 and buffer0 == 7:
			vJoy[JOY_DEV_0].y = readAxis()
	
		# z
		if channel == 2 and buffer0 == 7:
			vJoy[JOY_DEV_0].z = readAxis()
	
		# rx
		if channel == 3 and buffer0 == 7:
			vJoy[JOY_DEV_0].rx = readAxis()
	
		# ry
		if channel == 4 and buffer0 == 7:
			vJoy[JOY_DEV_0].ry = readAxis()
	
		# rz
		if channel == 5 and buffer0 == 7:
			vJoy[JOY_DEV_0].rz = readAxis()
	
		# slider
		if channel == 6 and buffer0 == 7:
			vJoy[JOY_DEV_0].slider = readAxis()
	
		# dial
		if channel == 7 and buffer0 == 7:
			vJoy[JOY_DEV_0].dial = readAxis()
	
	# POV Hat Switch - from Bank Select
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
			
		vJoy[JOY_DEV_0].setDigitalPov(0, povDirection)
	
	
	# Toggle buttons - from Activator, Solo/Cue, Record arm
	if status == MidiStatus.NoteOn or status == MidiStatus.NoteOff:
		
		# Activator - Buttons 1-8
		for c in range(8): 
			if channel == c and buffer0 == 50:
				buttonIndex = c + 0
				vJoy[JOY_DEV_0].setButton(buttonIndex, readButton())	
	
		# Solo / Cue - Buttons 11-18
		for c in range(8): 
			if channel == c and buffer0 == 49:
				buttonIndex = c + 10
				vJoy[JOY_DEV_0].setButton(buttonIndex, readButton())	
	
		# Record Arm - Buttons 21-28
		for c in range(8): 
			if channel == c and buffer0 == 48:
				buttonIndex = c + 20
				vJoy[JOY_DEV_0].setButton(buttonIndex, readButton())	
	

	######################
	### vJoy Device #2 ###
	######################	
	
	# Axis - from Track Control Encoders
	#if status == MidiStatus.Control and channel == 0:
	#
	#	# x
	#	if buffer0 == 48:
	#		vJoy[JOY_DEV_1].x = readAxis()
	#
	#	# y
	#	if buffer0 == 49:
	#		vJoy[JOY_DEV_1].y = readAxis()
	#
	#	# z
	#	if buffer0 == 50:
	#		vJoy[JOY_DEV_1].z = readAxis()
	#
	#	# rx
	#	if buffer0 == 51:
	#		vJoy[JOY_DEV_1].rx = readAxis()
	#
	#	# ry
	#	if buffer0 == 52:
	#		vJoy[JOY_DEV_1].ry = readAxis()
	#
	#	# rz
	#	if buffer0 == 53:
	#		vJoy[JOY_DEV_1].rz = readAxis()
	#
	#	# slider
	#	if buffer0 == 54:
	#		vJoy[JOY_DEV_1].slider = readAxis()
	#
	#	# dial
	#	if buffer0 == 55:
	#		vJoy[JOY_DEV_1].dial = readAxis()			
			
	
	# Momentary buttons - from Clip launch, Clip stop and Scene launch 
	if status == MidiStatus.NoteOn or status == MidiStatus.NoteOff:
		
		# Clip Launch - Buttons 1-8, 11-18, [...] through 48
		for c in range(8): # Channel
			for b in range(5): # Buffer0
				buttonMatrixY = b * 10 # Add 10 to each button row 
				buffer0Offset = 53 + b
				if channel == c and buffer0 == buffer0Offset:
					buttonIndex = buttonMatrixY + c # Add channel / column to row to get button index / number
					vJoy[JOY_DEV_1].setButton(buttonIndex, readButton())	
	
		# Scene Launch - Buttons 9, 19, 29, 39, 49
		for b in range(5):
			buttonMatrixY = (b * 10)
			buffer0Offset = 82 + b
			if channel == 0 and buffer0 == buffer0Offset:
				buttonIndex = buttonMatrixY + 8
				vJoy[JOY_DEV_1].setButton(buttonIndex, readButton())
	
		# Clip Stop - Buttons 51-58
		for c in range(8): 
			if channel == c and buffer0 == 52:
				buttonIndex = 50 + c
				vJoy[JOY_DEV_1].setButton(buttonIndex, readButton())	
		
		# Stop All Clips - Button 59 
		if channel == 0 and buffer0 == 81:
			vJoy[JOY_DEV_1].setButton(58, readButton())	

		# Track Control - Toggle buttons 61-64
		for b in range(4):
			buffer0Offset = 87 + b
			if channel == 0 and buffer0 == buffer0Offset:
				buttonIndex = b + 60
				vJoy[JOY_DEV_1].setButton(buttonIndex, readButton())
				
	# "Encoder like" buttons - from Device Control Encoders
	if status == MidiStatus.Control and channel == 0:
		# Button pairs: 9 and 10, 11 and 12 - up to 23 and 24
		# {{<MIDI buffer>:<vJoy button>}, [...]}
		encoderIndex = 0
		for key in range(48,56):
			if buffer0 == key:	
				currentEncoderState = readEncoder()				
				encoders[JOY_DEV_1][encoderIndex].updateEncoderButtonState(currentEncoderState)
			encoderIndex += 1

	######################
	### vJoy Device #3 ###
	######################
	
	# Axis - from Device Control Encoders
	# Channel 8 - Master Track. Device Control for Channel 0-7 is not mapped to any vJoy devices. Yet.
	#if status == MidiStatus.Control and channel == 8:
	#
	#	# x
	#	if buffer0 == 16:
	#		vJoy[JOY_DEV_2].x = readAxis()
	#
	#	# y
	#	if buffer0 == 17:
	#		vJoy[JOY_DEV_2].y = readAxis()
	#
	#	# z
	#	if buffer0 == 18:
	#		vJoy[JOY_DEV_2].z = readAxis()
	#
	#	# rx
	#	if buffer0 == 19:
	#		vJoy[JOY_DEV_2].rx = readAxis()
	#
	#	# ry
	#	if buffer0 == 20:
	#		vJoy[JOY_DEV_2].ry = readAxis()
	#
	#	# rz
	#	if buffer0 == 21:
	#		vJoy[JOY_DEV_2].rz = readAxis()
	#
	#	# slider
	#	if buffer0 == 22:
	#		vJoy[JOY_DEV_2].slider = readAxis()
	#
	#	# dial
	#	if buffer0 == 23:
	#		vJoy[JOY_DEV_2].dial = readAxis()
			
	# "Encoder like" buttons - from Device Control Encoders
	if status == MidiStatus.Control and channel == 8:
		# Button pairs: 9 and 10, 11 and 12 - up to 23 and 24
		# {{<MIDI buffer>:<vJoy button>}, [...]}
		encoderIndex = 0
		for key in range(16,24):
			if buffer0 == key:	
				currentEncoderState = readEncoder()				
				encoders[JOY_DEV_2][encoderIndex].updateEncoderButtonState(currentEncoderState)
			encoderIndex += 1
			
			
	

	# Momentary buttons - from Track Control
	if status == MidiStatus.NoteOn or status == MidiStatus.NoteOff:

		# Track Control - Buttons 1-8
		for b in range(8):
			buffer0Offset = 58 + b
			if channel == 8 and buffer0 == buffer0Offset:
				vJoy[JOY_DEV_2].setButton(b, readButton())


	######################
	### vJoy Device #4 ###
	######################
	
	# Axis - from Master slider and Balance slider
	if status == MidiStatus.Control and channel == 0:
		
		# x - Balance slider
		if buffer0 == 15:
			vJoy[JOY_DEV_3].x = readAxis()
	
		# y - Master slider
		if buffer0 == 14:
			vJoy[JOY_DEV_3].y = readAxis()

	# Buttons - from Misc
	if (status == MidiStatus.NoteOn or status == MidiStatus.NoteOff) and channel == 0:
	
		# Playback, Bank select, Tempo, Misc - Buttons 1-11
		for b in range(11):
			buffer0Offset = 91 + b
			if buffer0 == buffer0Offset:
				vJoy[JOY_DEV_3].setButton(b, readButton())	 

	# Encoder - from Cue Level
	if status == MidiStatus.Control and channel == 0 and buffer0 == 47:

		povMax = vJoy[JOY_DEV_3].continuousPovMax
		povIncrement = povMax / 100
		
		# MIDI signal is in lower 0-4 values when going up, and upper 123-127 when going down
		# POV value is held withing upper and lower limits
		# Up and Down buttons are triggered regardless of limits
		
		if buffer1 >= 120:
			vJoy[JOY_DEV_3].setPressed(11) # Encoder button down
			if povValue > 0:
				povValue -= povIncrement
			
		if buffer1 <= 10 :
			vJoy[JOY_DEV_3].setPressed(12) # Encoder button up
			if povValue < povMax:
				povValue += povIncrement
		
		vJoy[JOY_DEV_3].setAnalogPov(0, povValue)			
			


if starting:
	povValue = 0
	timepress = 0
	lastButtonPressed = 0

	encoders = {JOY_DEV_1:{}, JOY_DEV_2:{}}
	# Add 8 encoders to JOY_DEV_1
	for encIndex in range(8):
		buttonOffset = 64 + (encIndex * 2) 
		encoders[JOY_DEV_1][encIndex] = MidiEncoder(JOY_DEV_1, buttonOffset)

	# Add 8 encoders to JOY_DEV_2
	for encIndex in range(8):
		buttonOffset = 8 + (encIndex * 2) 
		encoders[JOY_DEV_2][encIndex] = MidiEncoder(JOY_DEV_2, buttonOffset)
		
	midi[MIDIDEVICE].update += update

# Check off timers on all encoders
for dev in encoders:
	for encoder in encoders[dev]:
		diagnostics.watch(encoders[dev][encoder].checkButtonOffDelay())


diagnostics.watch(encoders[JOY_DEV_2][0].buttonState)
diagnostics.watch(encoders[JOY_DEV_2][0].buttonActivatedClock)