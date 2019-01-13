# STEMMA_MIDI
### _A classic MIDI interface module compatible with the UART mode of Adafruit's STEMMA_

![Image of Module](https://github.com/CedarGroveStudios/STEMMA_MIDI/blob/master/2018-12-23%20STEMMA%20DIN-MIDI%20glamour%204w.png
)

The STEMMA MIDI interface is a self-powered, one-quarter protoboard-sized module for use with Adafruit STEMMA-compatible products. The interface converts incoming and outgoing classic MIDI current-loop input and output to STEMMA 3.3-volt logic. This interface requires that the host STEMMA interface be placed into UART mode with a fixed rate of 31,250 baud. 

The module has two ways to connect UART signals: a STEMMA-compatible 4-pin JST connection is provided on the top edge of the module, and two four-pin strips are available to allow header-style or soldered connections. The header-style connections allow the module to be used with UART signals from sources without a STEMMA interface connector. All power, ground, and RX/TX pins of these connectors are wired in parallel via printed circuit board traces.

The Type B (3.5mm TRS) MIDI input is an optically-isolated Type B 3.5mm TRS connection. The Type B (3.5mm TRS) MIDI output is buffered. On-board receive (RX) and transmit (TX) LEDs indicate incoming and outgoing MIDI signals. Interface module power is supplied by the STEMMA's 3.3-volt power pin.

The OSH Park STEMMA MIDI module project page: https://oshpark.com/shared_projects/qya9nIlp

The STEMMA MIDI interface was tested with CircuitPython version 3.1.1 and version 4.0.0 Alpha_5. Example test code for the Trellis M4 is provided in the repository.

![Image of Module](https://github.com/CedarGroveStudios/STEMMA_MIDI/blob/master/STEMMA%20MIDI%20v00%204w.jpg)
