import time
import mido

# List available MIDI devices
print("Available MIDI Output Ports:")
available_ports = mido.get_output_names()
print(available_ports)

# Use the detected MIDI device
output_name = 'UM-ONE'  # Replace this with the exact name shown in the available ports

# Check if the specified device is available
if output_name not in available_ports:
    raise ValueError(f"Device '{output_name}' not found. Check the available MIDI output ports.")

# Define the arpeggio notes (C Major chord: C, E, G)
notes = [60, 64, 67]  # MIDI notes for C, E, G

# Play the arpeggio on Channel 4 (index 3)
try:
    with mido.open_output(output_name) as outport:
        print("Starting arpeggio loop on MIDI Channel 4. Press Ctrl+C to stop.")
        while True:
            for note in notes:
                # Note On for MIDI Channel 4
                outport.send(mido.Message('note_on', note=note, velocity=64, channel=3))
                time.sleep(0.5)  # Delay between notes
                # Note Off for MIDI Channel 4
                outport.send(mido.Message('note_off', note=note, velocity=64, channel=3))
except KeyboardInterrupt:
    print("\nArpeggio loop stopped.")
