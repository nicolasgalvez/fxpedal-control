import rtmidi

midiout = rtmidi.MidiOut()
midiout.open_virtual_port("Guitarix Control")

# Send Program Change: preset 3
midiout.send_message([0xC0, 3])
print("Sent MIDI Program Change 3")
