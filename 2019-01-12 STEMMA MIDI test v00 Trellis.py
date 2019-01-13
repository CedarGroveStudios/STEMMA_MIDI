# 2019-01-12 STEMMA MIDI test v00 Trellis.py
# Simple MIDI send/receive test using UART
# via a custom "classic" MIDI interface
# Cedar Grove Studios 2019
#
# inspired by John Park's Classic MIDI Synth Control example code

import adafruit_trellism4

import board
import busio
uart = busio.UART(board.SDA, board.SCL, baudrate=31250, timeout=1)
print("MIDI UART EXAMPLE")

trellis = adafruit_trellism4.TrellisM4Express()
trellis.pixels.brightness = .1

# ## LISTS and DICTIONARIES ##
# MIDI Voice codes are contained in the Status_Byte (first message byte: Byte 0)
voice = {  # Status_Byte code: Voice_Name, Byte 1, Byte 2
    0x80 : ('Note_Off', 'Note', 'Vel'),
    0x90 : ('Note_On', 'Note', 'Vel'),
    0xA0 : ('Aftertouch', 'Note', 'Press'),
    0xB0 : ('Ctrl_Chg', 'Ctrl', 'Val'),
    0xC0 : ('Pgm_Chg', 'Pre_Num', ''),
    0xD0 : ('Chan_Press', 'Press', 'Press'),
    0xE0 : ('Pitch_Bend', 'Fine', 'Coarse'),
    0XF0 : ('Sys', 'Sys', 'Val')
    }

# MIDI System codes are extensions of the System Voice_Type (Byte 0)
system = {  # System code: Description, Byte 1, Byte 2
    0xF0 : ('Sys_Excl', 'Mfg_ID', '<data>'),
    0xF2 : ('Song_Pos', 'LSB', 'MSB'),
    0xF3 : ('Song_Sel', 'Song_Number', ''),
    0xF6 : ('Tune_Req', '', ''),
    0xF7 : ('EOX', '', '')
    }

# MIDI Controllers codes (definitions)
#   first byte received after the 0xB0 Ctrl_Chg Voice_Code (Byte 1)
#   0-63 continuous, 64-121 switch, 122-127 Chan_Mode
controllers = {  # Controller code: Ctrl_Name, Byte_2
    0 : ('Bank_Sel', 'Val'),
    1 : ('Mod', 'Val'),
    7 : ('Chan_Vol', 'Val'),
    11 : ('Exp_Pedal', 'Val'),
    64 : ('Sus_Damp_Pedal', 'Val'),
    120 : ('All_Sound_Off', 'Val'),
    121 : ('Reset_All_Ctrls', 'Val'),
    123 : ('All_Notes_Off', 'Val')
    }

# The DSP-G1 Control Codes are the synth's 19 controllable MIDI parameters
control_codes = [  # CC, V0(default)_Val, V1_Val, V2_Val, V3_Val, Module_Ctrl_Name
    (07, 127, 127, 127, 127, 127, 127, 'DCA_Mstr_Vol'),  # Amplifier
    (73, 0, 0, 0, 0, 0, 0, 'DCA_Att'),
    (75, 16, 16, 16, 16, 16, 16, 'DCA_Dec'),
    (31, 127, 127, 127, 127, 127, 127, 'DCA_Sus'),
    (72, 08, 08, 08, 08, 08, 08, 'DCA_Rel'),
    (74, 127, 127, 127, 127, 127, 127, 'LPF_Cutoff'),  # Low-Pass Filter
    (71, 0, 0, 0, 0, 0, 0, 'LPF_Res'),
    (01, 0, 0, 0, 0, 0, 0, 'LPF_LFO_Mod'),  # Low-Pass Filter Envelope
    (82, 0, 0, 0, 0, 0, 0, 'LPF_Att'),
    (83, 0, 0, 0, 0, 0, 0, 'LPF_Dec'),
    (28, 0, 0, 0, 0, 0, 0, 'LPF_Sus'),
    (29, 0, 0, 0, 0, 0, 0, 'LPF_Rel'),
    (81, 0, 0, 0, 0, 0, 0, 'LPF_Env_Mod'),
    (20, 0, 0, 0, 0, 0, 0, 'LFO_Wave'),  # Low-Freq Oscillator
    (16, 0, 0, 0, 0, 0, 0, 'LFO_Freq'),
    (76, 127, 127, 127, 127, 127, 127, 'DCO_Wave'),  # Note Oscillators
    (21, 64, 64, 64, 64, 64, 64, 'DCO_Range'),
    (93, 0, 0, 0, 0, 0, 0, 'DCO_Detune'),
    (04, 0, 0, 0, 0, 0, 0, 'DCO_Wrap_Mod')
]

note_base = {
    0 : 'C',
    1 : 'C#',
    2 : 'D',
    3 : 'D#',
    4 : 'E',
    5 : 'F',
    6 : 'F#',
    7 : 'G',
    8 : 'G#',
    9 : 'A',
    10 : 'A#',
    11 : 'B'
    }

blk_keys = [ 1, 3, 6, 8, 10 ]

# ## HELPERS ##
def note_name(note):  # converts a sequential note value to a note name
    name = note_base[note % 12] + str(int((note - (note % 12))/12))
    return name

for y in range(trellis.pixels.height):
    for x in range(trellis.pixels.width):
        # print(((y * 8) + x)//12, ((y * 8) + x)%12)
        if ((y * 8) + x) % 12 in blk_keys: trellis.pixels[x, y] = 0x040404
        else: trellis.pixels[x, y] = 0xffffff
        pixel_index = (((y * 8) + x) * 256 // 2)

current_press = set()

while True:
    pressed = set(trellis.pressed_keys)

    for press in pressed - current_press:
        x, y = press
        note_val = 36 + x + (y * 8)
        trellis.pixels[x, y] = 0xff0000
        print("Trellis note_on :", note_name(note_val), note_val, press)
        uart.write(bytes([0x90, note_val, 100]))

    for release in current_press - pressed:
        x, y = release
        note_val = 36 + x + (y * 8)
        if ((y * 8) + x) % 12 in blk_keys: trellis.pixels[x, y] = 0x040404
        else: trellis.pixels[x, y] = 0xffffff
        print("Trellis note_off:", note_name(note_val), note_val, release)
        uart.write(bytes([0x90, note_val, 0]))  # note off

    current_press = pressed
    
    data = uart.read(1)  # get a byte from RX
    if data is not None:
        if data[0] & 0x80:  # status byte
            byte_count = 0
            try:  # check for valid voice_type
                status = voice[data[0] & 0xF0]
                chan = data[0] & 0x0F
                valid_message = True
            except:
                valid_message = False
        elif valid_message:
            if status[1] == 'Note':
                valid_message = True
                if byte_count % 2:  # odd byte count (Byte 1, 3, etc.)
                    note_val = data[0]
                    print("  ", status[1], data[0], "("+note_name(data[0])+")")
                else:  # even byte count (Byte 2, 4, etc.)
                    print("  ", status[2], data[0])
                    if data[0] > 0:
                        if note_val > 32 and note_val < 68:
                            print("MIDI --> Trellis note_on", note_val)
                            x = (note_val - 36) % 8
                            y = (note_val - 36) // 8
                            print(x,y)
                            trellis.pixels[x, y] = 0xff0000
                        else: print ("Note outside of Trellis range")
                    else:
                        if note_val > 32 and note_val < 68:
                            print("MIDI --> Trellis note_off", note_val)
                            x = (note_val - 36) % 8
                            y = (note_val - 36) // 8
                            print(x,y)
                            if ((y * 8) + x) % 12 in blk_keys: trellis.pixels[x, y] = 0x040404
                            else: trellis.pixels[x, y] = 0xffffff
                        else: print ("Note outside of Trellis range")    
            if status[1] != 'Note':
                valid_message = True
                if byte_count % 2:  # odd byte count (Byte 1, 3, etc.)
                    print("  ", status[1], data[0])
                else:  # even byte count (Byte 2, 4, etc.)
                    print("  ", status[2], data[0])
        byte_count = byte_count + 1
        uart.write(data)  # transmit bytearray
