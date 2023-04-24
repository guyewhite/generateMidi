# generateMidi.py
# A useful tool create midi files for one or more of the chord scales, v1
#
# G. Elvin White
# 24 April 2023
# www.gelvinwhite.com
#
# Usage:    ./python3 generateMidi [bpm] [seconds per note] [velocity]
# Example:  ./python3 generateMidi 120 2 127
#           This example generates all midi chords for two seconds each at 120 beats per minute.
#
# Usage:    ./python3 generateMidi
# Example:  ./python3 generateMidi
#           This example generates all midi chords using the default settings of 1 second midi files at 120 beats per minute.

# Import necessary libraries
import os
import sys
import mido
from mido import MidiFile, MidiTrack, Message
import roman
import time

# Define all the chord scales
chordScales = {
    'Cmaj': ['Cmaj', 'Dm', 'Em', 'Fmaj', 'Gmaj', 'Am', 'Bdim'],
    'Dmaj': ['Dmaj', 'Em', 'F#m', 'Gmaj', 'Amaj', 'Bm', 'C#dim'],
    'Emaj': ['Emaj', 'F#m', 'G#m', 'Amaj', 'Bmaj', 'C#m', 'D#dim'],
    'Fmaj': ['Fmaj', 'Gm', 'Am', 'Bbmaj', 'Cmaj', 'Dm', 'Edim'],
    'Gmaj': ['Gmaj', 'Am', 'Bm', 'Cmaj', 'Dmaj', 'Em', 'F#dim'],
    'Amaj': ['Amaj', 'Bm', 'C#m', 'Dmaj', 'Emaj', 'F#m', 'G#dim'],
    'Bmaj': ['Bmaj', 'C#m', 'D#m', 'Emaj', 'F#maj', 'G#m', 'A#dim'],
    'C#maj': ['C#maj', 'D#m', 'E#m', 'F#maj', 'G#maj', 'A#m', 'B#dim'],
    'F#maj': ['F#maj', 'G#m', 'A#m', 'Bmaj', 'C#maj', 'D#m', 'E#dim'],
    'Abmaj': ['Abmaj', 'Bbm', 'Cm', 'Dbmaj', 'Ebmaj', 'Fm', 'Gdim'],
    'Bbmaj': ['Bbmaj', 'Cm', 'Dm', 'Ebmaj', 'Fmaj', 'Gm', 'Adim'],
    'Cbmaj': ['Cbmaj', 'Dbm', 'Ebm', 'Fbmaj', 'Gbmaj', 'Abm', 'Bbdim'],
    'Dbmaj': ['Dbmaj', 'Ebm', 'Fm', 'Gbmaj', 'Abmaj', 'Bbm', 'Cdim'],
    'Ebmaj': ['Ebmaj', 'Fm', 'Gm', 'Abmaj', 'Bbmaj', 'Cm', 'Ddim'],
    'Cm': ['Cm', 'Ddim', 'Ebmaj', 'Fm', 'Gm', 'Abmaj', 'Bbmaj'],
    'Dm': ['Dm', 'Edim', 'Fmaj', 'Gmaj', 'Am', 'Bbmaj', 'Cmaj'],
    'Em': ['Em', 'F#dim', 'Gmaj', 'Am', 'Bm', 'Cmaj', 'Dmaj'],
    'Fm': ['Fm', 'Gdim', 'Abmaj', 'Bbmaj', 'Cm', 'Dbmaj', 'Ebmaj'],
    'Gm': ['Gm', 'Adim', 'Bbmaj', 'Cm', 'Dm', 'Ebmaj', 'Fmaj'],
    'Am': ['Am', 'Bdim', 'Cmaj', 'Dm', 'Em', 'Fmaj', 'Gmaj'],
    'Bm': ['Bm', 'C#dim', 'Dmaj', 'Em', 'F#m', 'Gmaj', 'Amaj'],
    'F#m': ['F#m', 'G#dim', 'Amaj', 'Bm', 'C#m', 'Dmaj', 'Emaj'],
    'C#m': ['C#m', 'D#dim', 'Emaj', 'F#m', 'G#m', 'Amaj', 'Bmaj'],
    'G#m': ['G#m', 'A#dim', 'Bmaj', 'C#m', 'D#m', 'Emaj', 'F#maj'],
    'D#m': ['D#m', 'E#dim', 'F#maj', 'G#m', 'A#m', 'Bmaj', 'C#maj'],
    'A#m': ['A#m', 'B#dim', 'C#maj', 'D#m', 'E#m', 'F#maj', 'G#maj'],
    'Bbm': ['Bbm', 'Cdim', 'Dbmaj', 'Ebm', 'Fm', 'Gbmaj', 'Abmaj'],
    'Ebm': ['Ebm', 'Fdim', 'Gbmaj', 'Abm', 'Bbm', 'Cbmaj', 'Dbmaj'],
    'Abm': ['Abm', 'Bbdim', 'Cbmaj', 'Dbm', 'Ebm', 'Fbmaj', 'Gbmaj'],
    'Cmaj7': ['Cmaj7', 'Dm7', 'Em7', 'Fmaj7', 'G7', 'Am7', 'Bhalf-dim7'],
    'Dmaj7': ['Dmaj7', 'Em7', 'F#m7', 'Gmaj7', 'A7', 'Bm7', 'C#half-dim7'],
    'Emaj7': ['Emaj7', 'F#m7', 'G#m7', 'Amaj7', 'B7', 'C#m7', 'D#half-dim7'],
    'Fmaj7': ['Fmaj7', 'Gm7', 'Am7', 'Bbmaj7', 'C7', 'Dm7', 'Ehalf-dim7'],
    'Gmaj7': ['Gmaj7', 'Am7', 'Bm7', 'Cmaj7', 'D7', 'Em7', 'F#half-dim7'],
    'Amaj7': ['Amaj7', 'Bm7', 'C#m7', 'Dmaj7', 'E7', 'F#m7', 'G#half-dim7'],
    'Bmaj7': ['Bmaj7', 'C#m7', 'D#m7', 'Emaj7', 'F#7', 'G#m7', 'A#half-dim7'],
    'C#maj7': ['C#maj7', 'D#m7', 'E#m7', 'F#maj7', 'G#7', 'A#m7', 'B#half-dim7'],
    'F#maj7': ['F#maj7', 'G#m7', 'A#m7', 'Bmaj7', 'C#7', 'D#m7', 'E#half-dim7'],
    'Abmaj7': ['Abmaj7', 'Bbm7', 'Cm7', 'Dbmaj7', 'Eb7', 'Fm7', 'Ghalf-dim7'],
    'Bbmaj7': ['Bbmaj7', 'Cm7', 'Dm7', 'Ebmaj7', 'F7', 'Gm7', 'Ahalf-dim7'],
    'Cbmaj7': ['Cbmaj7', 'Dbm7', 'Ebm7', 'Fbmaj7', 'Gb7', 'Abm7', 'Bbhalf-dim7'],
    'Dbmaj7': ['Dbmaj7', 'Ebm7', 'Fm7', 'Gbmaj7', 'Ab7', 'Bbm7', 'Chalf-dim7'],
    'Ebmaj7': ['Ebmaj7', 'Fm7', 'Gm7', 'Abmaj7', 'Bb7', 'Cm7', 'Dhalf-dim7'],
    'Cm7': ['Cm7', 'Dhalf-dim7', 'Ebmaj7', 'Fm7', 'Gm7', 'Abmaj7', 'Bbdom7'],
    'Dm7': ['Dm7', 'Ehalf-dim7', 'Fmaj7', 'Gm7', 'Am7', 'Bbmaj7', 'Cdom7'],
    'Em7': ['Em7', 'F#half-dim7', 'Gmaj7', 'Am7', 'Bm7', 'Cmaj7', 'Ddom7'],
    'Fm7': ['Fm7', 'Ghalf-dim7', 'Abmaj7', 'Bbm7', 'Cm7', 'Dbmaj7', 'Ebdom7'],
    'Gm7': ['Gm7', 'Ahalf-dim7', 'Bbmaj7', 'Cm7', 'Dm7', 'Ebmaj7', 'Fdom7'],
    'Am7': ['Am7', 'Bhalf-dim7', 'Cmaj7', 'Dm7', 'Em7', 'Fmaj7', 'Gdom7'],
    'Bm7': ['Bm7', 'C#half-dim7', 'Dmaj7', 'Em7', 'F#m7', 'Gmaj7', 'Adom7'],
    'F#m7': ['F#m7', 'G#half-dim7', 'Amaj7', 'Bm7', 'C#m7', 'Dmaj7', 'E7'],
    'C#m7': ['C#m7', 'D#half-dim7', 'Emaj7', 'F#m7', 'G#m7', 'Amaj7', 'Bdom7'],
    'G#m7': ['G#m7', 'A#half-dim7', 'Bmaj7', 'C#m7', 'D#m7', 'Emaj7', 'F#dom7'],
    'D#m7': ['D#m7', 'E#half-dim7', 'F#maj7', 'G#m7', 'A#m7', 'Bmaj7', 'C#dom7'],
    'A#m7': ['A#m7', 'B#half-dim7', 'C#maj7', 'D#m7', 'E#m7', 'F#maj7', 'G#dom7'],
    'Bbm7': ['Bbm7', 'Chalf-dim7', 'Dbmaj7', 'Ebm7', 'Fm7', 'Gbmaj7', 'Abdom7'],
    'Ebm7': ['Ebm7', 'Fhalf-dim7', 'Gbmaj7', 'Abm7', 'Bbm7', 'Cbmaj7', 'Dbdom7'],
    'Abm7': ['Abm7', 'Bbhalf-dim7', 'Cbmaj7', 'Dbm7', 'Ebm7', 'Fbmaj7', 'Gbdom7'],
}

# Define all the notes of each chord.
individualChords = {
    'Amaj': ['A', 'C#', 'E'],
    'A#dim': ['A#', 'C#', 'E'],
    'A#m': ['A#', 'C#', 'E#'],
    'Abmaj': ['Ab', 'C', 'Eb'],
    'Abm': ['Ab', 'B', 'Eb'],
    'Abdim': ['Ab', 'B', 'D'],
    'Adim': ['A', 'C', 'Eb'],
    'Am': ['A', 'C', 'E'],
    'Bmaj': ['B', 'D#', 'F#'],
    'B#dim': ['B#', 'D#', 'F#'],
    'Bbmaj': ['Bb', 'D', 'F'],
    'Bbdim': ['Bb', 'Db', 'E'],
    'Bbm': ['Bb', 'Db', 'F'],
    'Bdim': ['B', 'D', 'F'],
    'Bm': ['B', 'D', 'F#'],
    'Cmaj': ['C', 'E', 'G'],
    'C#maj': ['C#', 'E#', 'G#'],
    'C#dim': ['C#', 'E', 'G'],
    'C#m': ['C#', 'E', 'G#'],
    'Cbdim': ['Cb', 'E', 'G'],
    'Cbmaj': ['Cb', 'Eb', 'Gb'],
    'Cdim': ['C', 'Eb', 'Gb'],
    'Cm': ['C', 'Eb', 'G'],
    'Dmaj': ['D', 'F#', 'A'],
    'D#dim': ['D#', 'F#', 'A'],
    'D#m': ['D#', 'F#', 'A#'],
    'Dbmaj': ['Db', 'F', 'Ab'],
    'Dbdim': ['Db', 'Fb', 'G'],
    'Dbm': ['Db', 'E', 'Ab'],
    'Ddim': ['D', 'F', 'Ab'],
    'Dm': ['D', 'F', 'A'],
    'Emaj': ['E', 'G#', 'B'],
    'E#dim': ['E#', 'G#', 'B'],
    'E#m': ['E#', 'G#', 'B#'],
    'Ebmaj': ['Eb', 'G', 'Bb'],
    'Ebm': ['Eb', 'Gb', 'Bb'],
    'Ebdim': ['Eb', 'Gb', 'A'],
    'Edim': ['E', 'G', 'Bb'],
    'Em': ['E', 'G', 'B'],
    'Fmaj': ['F', 'A', 'C'],
    'F#maj': ['F#', 'A#', 'C#'],
    'F#dim': ['F#', 'A', 'C'],
    'F#m': ['F#', 'A', 'C#'],
    'Fbmaj': ['Fb', 'Ab', 'Cb'],
    'Fbdim': ['Fb', 'G', 'Bb'],
    'Fdim': ['F', 'Ab', 'B'],
    'Fm': ['F', 'Ab', 'C'],
    'Gmaj': ['G', 'B', 'D'],
    'G#maj': ['G#', 'B#', 'D#'],
    'G#dim': ['G#', 'B', 'D'],
    'G#m': ['G#', 'B', 'D#'],
    'Gbmaj': ['Gb', 'Bb', 'Db'],
    'Gbdim': ['Gb', 'A', 'C'],
    'Gdim': ['G', 'Bb', 'Db'],
    'Gbm': ['Gb', 'A', 'Db'],
    'Gm': ['G', 'Bb', 'D'],
    'Cmaj7': ['C', 'E', 'G', 'B'],
    'Dmaj7': ['D', 'F#', 'A', 'C#'],
    'Emaj7': ['E', 'G#', 'B', 'D#'],
    'Fmaj7': ['F', 'A', 'C', 'E'],
    'Gmaj7': ['G', 'B', 'D', 'F#'],
    'Amaj7': ['A', 'C#', 'E', 'G#'],
    'Bmaj7': ['B', 'D#', 'F#', 'A#'],
    'C#maj7': ['C#', 'E#', 'G#', 'B#'],
    'F#maj7': ['F#', 'A#', 'C#', 'E#'],
    'Abmaj7': ['Ab', 'C', 'Eb', 'G'],
    'Bbmaj7': ['Bb', 'D', 'F', 'A'],
    'Cbmaj7': ['Cb', 'Eb', 'Gb', 'Bb'],
    'Dbmaj7': ['Db', 'F', 'Ab', 'C'],
    'Ebmaj7': ['Eb', 'G', 'Bb', 'D'],
    'Fbmaj7': ['Fb', 'Ab', 'Cb', 'Eb'],
    'Gbmaj7': ['Gb', 'Bb', 'Db', 'F'],
    'Dm7': ['D', 'F', 'A', 'C'],
    'Em7': ['E', 'G', 'B', 'D'],
    'F#m7': ['F#', 'A', 'C#', 'E'],
    'Gm7': ['G', 'Bb', 'D', 'F'],
    'Am7': ['A', 'C', 'E', 'G'],
    'Bm7': ['B', 'D', 'F#', 'A'],
    'C#m7': ['C#', 'E', 'G#', 'B'],
    'D#m7': ['D#', 'F#', 'A#', 'C#'],
    'G#m7': ['G#', 'B', 'D#', 'F#'],
    'Bbm7': ['Bb', 'Db', 'F', 'Ab'],
    'Cm7': ['C', 'Eb', 'G', 'Bb'],
    'Dbm7': ['Db', 'E', 'Ab', 'Cb'],
    'Ebm7': ['Eb', 'Gb', 'Bb', 'Db'],
    'Fm7': ['F', 'Ab', 'C', 'Eb'],
    'E#m7': ['E#', 'G#', 'B#', 'D#'],
    'A#m7': ['A#', 'C#', 'E#', 'G#'],
    'Abm7': ['Ab', 'B', 'Eb', 'Gb'],
    'Am7b5': ['A', 'C', 'Eb', 'G'],
    'Bm7b5': ['B', 'D', 'F', 'A'],
    'Cm7b5': ['C', 'Eb', 'Gb', 'Bb'],
    'C#m7b5': ['C#', 'E', 'G', 'B'],
    'Dm7b5': ['D', 'F', 'Ab', 'C'],
    'Ebm7b5': ['Eb', 'Gb', 'A', 'Db'],
    'Em7b5': ['E', 'G', 'Bb', 'D'],
    'Fm7b5': ['F', 'Ab', 'B', 'Eb'],
    'F#m7b5': ['F#', 'A', 'C', 'E'],
    'Gm7b5': ['G', 'Bb', 'Db', 'F'],
    'Abm7b5': ['Ab', 'B', 'D', 'Gb'],
    'A#m7b5': ['A#', 'C#', 'E', 'G#'],
    'Bbm7b5': ['Bb', 'Db', 'E', 'Ab'],
    'C7': ['C', 'E', 'G', 'Bb'],
    'D7': ['D', 'F#', 'A', 'C'],
    'E7': ['E', 'G#', 'B', 'D'],
    'F7': ['F', 'A', 'C', 'Eb'],
    'G7': ['G', 'B', 'D', 'F'],
    'A7': ['A', 'C#', 'E', 'G'],
    'B7': ['B', 'D#', 'F#', 'A'],
    'C#7': ['C#', 'E#', 'G#', 'B'],
    'D#7': ['D#', 'F##', 'A#', 'C#'],
    'F#7': ['F#', 'A#', 'C#', 'E'],
    'G#7': ['G#', 'B#', 'D#', 'F#'],
    'Ab7': ['Ab', 'C', 'Eb', 'Gb'],
    'Bb7': ['Bb', 'D', 'F', 'Ab'],
    'Cb7': ['Cb', 'Eb', 'Gb', 'A'],
    'Db7': ['Db', 'F', 'Ab', 'Cb'],
    'Eb7': ['Eb', 'G', 'Bb', 'Db'],
    'Fb7': ['Fb', 'Ab', 'Cb', 'E'],
    'Gb7': ['Gb', 'Bb', 'Db', 'F'],
    'Bhalf-dim7': ['B', 'D', 'F', 'A'],
    'C#half-dim7': ['C#', 'E', 'G', 'B'],
    'D#half-dim7': ['D#', 'F#', 'A', 'C#'],
    'Ehalf-dim7': ['E', 'G', 'Bb', 'D'],
    'F#half-dim7': ['F#', 'A', 'C', 'E'],
    'G#half-dim7': ['G#', 'B', 'D', 'F#'],
    'A#half-dim7': ['A#', 'C#', 'E', 'G#'],
    'B#half-dim7': ['B#', 'D#', 'F#', 'A#'],
    'E#half-dim7': ['E#', 'G#', 'B', 'D#'],
    'Ghalf-dim7': ['G', 'Bb', 'Db', 'F'],
    'Ahalf-dim7': ['A', 'C', 'Eb', 'G'],
    'Bbhalf-dim7': ['Bb', 'Db', 'Fb', 'Ab'],
    'Chalf-dim7': ['C', 'Eb', 'Gb', 'Bb'],
    'Dhalf-dim7': ['D', 'F', 'Ab', 'C'],
    'Fhalf-dim7': ['F', 'Ab', 'Cb', 'Eb'],
    'Fhalf-dim7': ['F', 'Ab', 'Cb', 'Eb'],
    'Adom7': ['A', 'C#', 'E', 'G'],
    'Bdom7': ['B', 'D#', 'F#', 'A'],
    'Cdom7': ['C', 'E', 'G', 'Bb'],
    'Ddom7': ['D', 'F#', 'A', 'C'],
    'Fdom7': ['F', 'A', 'C', 'Eb'],
    'Gdom7': ['G', 'B', 'D', 'F'],
    'C#dom7': ['C#', 'E#', 'G#', 'B'],
    'F#dom7': ['F#', 'A#', 'C#', 'E'],
    'G#dom7': ['G#', 'B#', 'D#', 'F#'],
    'Abdom7': ['Ab', 'C', 'Eb', 'Gb'],
    'Bbdom7': ['Bb', 'D', 'F', 'Ab'],
    'Dbdom7': ['Db', 'F', 'Ab', 'Cb'],
    'Ebdom7': ['Eb', 'G', 'Bb', 'Db'],
    'Gbdom7': ['Gb', 'Bb', 'Db', 'Fb']
}

# Define the midi value of each note
note_dict = {
    'Ab': 68,
    'A': 69,
    'A#': 70,
    'Bb': 70,
    'B': 71,
    'B#': 72,
    'Cb': 59,
    'C': 60,
    'C#': 61,
    'Db': 61,
    'D': 62,
    'D#': 63,
    'Eb': 63,
    'E': 64,
    'E#': 65,
    'Fb': 64,
    'F': 65,
    'F#': 66,
    'Gb': 66,
    'G': 67,
    'G#': 68
}

# Grab User Input
args = sys.argv
if len(args) == 1:
    userTempo = 120
    userTime = 1
    userVelocity=127
elif len(args) > 4:
    print("usage: ./python3 generateMidi [bpm] [seconds] [velocity]")
    exit()
else:
    userTempo = int(args[1])
    userTime = int(args[2])
    userVelocity = int(args[3])

# Create a main directory to store the chord scale folders
main_directory = "Chord_Scales"
if not os.path.exists(main_directory):
    os.makedirs(main_directory)

#define tempo
tempo = mido.bpm2tempo(userTempo)

# Create a folder for each chord scale
for scale, chords in chordScales.items():
    scale_directory = os.path.join(main_directory, scale)
    
    if not os.path.exists(scale_directory):
        os.makedirs(scale_directory)

    # Create one file with all the chords
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)

    #add scale name as track
    chordName = f"{scale}"
    chordFileName = f"{scale} Scale.mid"
    title_msg = mido.MetaMessage('track_name', name=chordName)
    track.append(title_msg)

    # find first note
    lowestNote = (note_dict[individualChords[scale][0]])
  
    # generate full chord scale midi file
    duration = userTime
    prevRootMidiValue = 0
    for index, chord in enumerate(chords, start=1):

        # ensure the chord is present in the individualChords above
        if chord in individualChords:

            # get a list of all the notes of this one chord
            notes = individualChords[chord]

            # define the root note of this one chord
            rootNote = note_dict[notes[0]]

            # set some initial values for our for loop below, including the length of the notes per user input at the command line
            time_ticks = int(userTime * mido.second2tick(1, midi.ticks_per_beat, tempo))
            firstNote = True

            # create the note_on values for each of the notes, all starting at the same time
            for note in notes:

                # find the midi value of this one note
                midiValue = note_dict[note]

                # ensure that this note is not lower than a previous note
                while midiValue < rootNote or midiValue < lowestNote or midiValue <= prevRootMidiValue:
                    midiValue = midiValue + 12
               
                # append this midi information to the midi track
                track.append(Message('note_on', note=midiValue, velocity=userVelocity, time=0))
            
            # create the note_off values for each of the notes
            for note in notes:

                # find the midi value of this one note
                midiValue = note_dict[note]

                # ensure that this note is not lower than a previous note
                while midiValue < rootNote or midiValue < lowestNote or midiValue <= prevRootMidiValue:
                    midiValue = midiValue + 12
               
                # if it's the first note, turn the note off at the right user-defined interval. Also, define the root note used in this chord.
                if firstNote == True:

                    # append this midi information to the midi track
                    track.append(Message('note_off', note=midiValue, velocity=userVelocity, time=time_ticks))

                    # record the root note of this current chord such that no future root will be lower
                    prevRootMidiValue = midiValue 

                    # toggle the firstNote, as the next note is no longer the first
                    firstNote = False
                else:

                    # if not the first note, record this midi information at a time index of zero, exactly where the "firstNote" ended.
                    track.append(Message('note_off', note=midiValue, velocity=userVelocity, time=0))
    
    # save the entire scale
    full_file_path = os.path.join(scale_directory, chordFileName)
    midi.save(full_file_path)

    # reset values
    firstNote = True

    # Create Each Individual Chord
    for index, chord in enumerate(chords, start=1):

         # Create one file for each chorrd
        midi = MidiFile()
        track = MidiTrack()
        midi.tracks.append(track)

        # determine some information about this chord so we can record its name
        scaleDegree = roman.toRoman(index)
        decorate = ""
        if "maj" not in chord:
            scaleDegree = scaleDegree.lower()
        if "dim" in chord:
            decorate = "°"
        if "7" in chord:
            if "maj" in chord:
                decorate = "maj"

        # create the internal midi track name and filename for the chord
        chordName = f"{index} - {scaleDegree}{decorate} - {chord}"
        chordFileName = f"{chordName}.mid"

        #add chord name as track
        title_msg = mido.MetaMessage('track_name', name=chordName)
        track.append(title_msg)

        # ensure the chord is present in the individualChords above
        if chord in individualChords:

            # get a list of all the notes of this one chord
            notes = individualChords[chord]

            # define the root note of this one chord
            rootNote = note_dict[notes[0]]

            # create the note_on messages for each note
            for note in notes:

                # find the midi value of this one note
                midiValue = note_dict[note]

                # ensure all notes are greater or equal to the root
                if midiValue < rootNote:
                    midiValue = midiValue + 12
               
                # add the note_on message
                track.append(Message('note_on', note=midiValue, velocity=userVelocity, time=0))

                # define the passage of time
                time_ticks = int(userTime * mido.second2tick(1, midi.ticks_per_beat, tempo))

            # create the note_off values for each of the notes
            for note in notes:

                # find the midi value of this one note
                midiValue = note_dict[note]
               
                # if it's the first note, turn the note off at the right user-defined interval. Also, define the root note used in this chord.
                if firstNote == True:

                    # append this midi information to the midi track
                    track.append(Message('note_off', note=midiValue, velocity=userVelocity, time=time_ticks))

                    # toggle the firstNote, as the next note is no longer the first
                    firstNote = False
                else:

                    # if not the first note, record this midi information at a time index of zero, exactly where the "firstNote" ended.
                    track.append(Message('note_off', note=midiValue, velocity=userVelocity, time=0))

            firstNote = True

        # Note any errors
        else:
            print("Error at " + chordName)

        # save each file
        full_file_path = os.path.join(scale_directory, chordFileName)
        midi.save(full_file_path)