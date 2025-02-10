import time
import mido
import os

# List available MIDI devices
print("Available MIDI Output Ports:")
available_ports = mido.get_output_names()
print(available_ports)

# Specify the MIDI output port (adjust if necessary)
output_name = 'UM-ONE'  # Replace this with the correct device name from the list

# Check if the specified device is available
if output_name not in available_ports:
    raise ValueError(f"Device '{output_name}' not found. Check the available MIDI output ports.")

# Directory containing MIDI files
midi_folder_path = 'path/to/your/midi/folder'

# Set BPM and calculate delay between notes
bpm = 156
delay = 60 / bpm  # Convert BPM to delay in seconds

# Function to extract note-on events from all MIDI files in the folder
def extract_notes_from_folder(folder_path):
    notes = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.mid') or file_name.endswith('.midi'):
            midi_file = mido.MidiFile(os.path.join(folder_path, file_name))
            for track in midi_file.tracks:
                for msg in track:
                    if msg.type == 'note_on' and msg.velocity > 0:
                        notes.append(msg.note)
    return notes

# Extract notes from all MIDI files in the folder
notes = extract_notes_from_folder(midi_folder_path)
print(f"Total extracted notes: {notes}")

# Play the notes on MIDI Channel 4 (index 3)
try:
    with mido.open_output(output_name) as outport:
        print(f"Starting arpeggio loop on MIDI Channel 4 at {bpm} BPM. Press Ctrl+C to stop.")
        while True:
            for note in notes:
                # Note On for MIDI Channel 4
                outport.send(mido.Message('note_on', note=note, velocity=64, channel=3))
                time.sleep(delay)  # Delay based on BPM
                # Note Off for MIDI Channel 4
                outport.send(mido.Message('note_off', note=note, velocity=64, channel=3))
except KeyboardInterrupt:
    print("\nArpeggio loop stopped.")