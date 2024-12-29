import rtmidi
import time

# Note names mapping
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Extended chord intervals in semitones
CHORD_PATTERNS = {
    'Major': [0, 4, 7],
    'Minor': [0, 3, 7],
    'Diminished': [0, 3, 6],
    'Augmented': [0, 4, 8],
    'Major 7th': [0, 4, 7, 11],
    'Minor 7th': [0, 3, 7, 10],
    '6th': [0, 4, 7, 9],
    '9th': [0, 4, 7, 11, 14],
    'Suspended 2nd (sus2)': [0, 2, 7],
    'Suspended 4th (sus4)': [0, 5, 7],
}

def get_note_name(note_value):
    """Convert a MIDI note value to its name."""
    octave = (note_value // 12) - 1
    note_name = NOTE_NAMES[note_value % 12]
    return f"{note_name}{octave}"

def detect_chord(notes):
    """Detect the chord from a set of notes."""
    sorted_notes = sorted(notes)
    root_note = sorted_notes[0]
    root_name = NOTE_NAMES[root_note % 12]  # Extract root note name without octave
    intervals = [(note - root_note) % 12 for note in sorted_notes]
    for chord_name, pattern in CHORD_PATTERNS.items():
        if all(interval in intervals for interval in pattern):
            return root_name, chord_name
    return root_name, "Unknown"

# Initialize MIDI input
midiin = rtmidi.MidiIn()
available_ports = midiin.get_ports()

if not available_ports:
    print("No MIDI input ports available.")
else:
    print("Available MIDI Input Ports:")
    for i, port_name in enumerate(available_ports):
        print(f"[{i}] {port_name}")

    # Select the UM-ONE port
    for i, port_name in enumerate(available_ports):
        if "UM-ONE" in port_name:
            um_one_port = i
            break
    else:
        print("UM-ONE MIDI device not found.")
        exit(1)

    # Open the UM-ONE port
    midiin.open_port(um_one_port)
    print(f"Listening to MIDI on: {available_ports[um_one_port]}")

    active_notes = set()

    try:
        while True:
            message = midiin.get_message()
            if message:
                msg, delta_time = message
                status_byte = msg[0] & 0xF0
                note_value = msg[1]

                if status_byte == 0x90 and msg[2] > 0:  # Note-on
                    active_notes.add(note_value)

                elif status_byte == 0x80 or (status_byte == 0x90 and msg[2] == 0):  # Note-off
                    active_notes.discard(note_value)

                # Detect and print the chord
                if len(active_notes) >= 2:
                    root_note, chord_name = detect_chord(active_notes)
                    if chord_name != "Unknown":
                        note_names = [get_note_name(note) for note in sorted(active_notes)]
                        print(f"Chord Detected: {root_note} {chord_name} [{', '.join(note_names)}]")

    except KeyboardInterrupt:
        print("\nExiting MIDI listener.")

    midiin.close_port()
