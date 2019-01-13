# STEMMA_MIDI
### _A classic MIDI interface module compatible with Adafruit's STEMMA UART mode_

![Image of Yaktocat](https://octodex.github.com/images/yaktocat.png)

The STEMMA MIDI interface is a self-powered, one-quarter protoboard-sized module for use with Adafruit STEMMA-compatible products. The interface converts incoming and outgoing classic MIDI current-loop input and output for the STEMMA's 3.3-volt logic. This interface requires that the STEMMA interface be placed into UART mode with a fixed baud rate of 31,250. 

The module has two ways to connect UART signals: a STEMMA-compatible 4-pin JST connection is provided on the top edge of the module, and two four-pin strips are available to allow header-style or soldered connections. All power, ground, RX, and TX pins on these connectors are wired in parallel. The header-style connections allow the module to be used with UART signals from sources without a STEMMA interface connector.

The Type B (3.5mm TRS) MIDI input is an optically-isolated Type B 3.5mm TRS connection. The Type B (3.5mm TRS) MIDI output is buffered. On-board receive (RX) and transmit (TX) LEDs indicate incoming and outgoing MIDI signals. Interface module power is supplied by the STEMMA's 3.3-volt power pin.

The STEMMA MIDI interface was tested with CircuitPython version 3.1.1 and version 4.0.0 Alpha_5. Example test code for the Trellis M4 is provided in the repository.