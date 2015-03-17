# hayes-mouse

Arduino and Python code for mouse control using a classic analog Hayes joystick

The Arduino polls two pins configured as ADCs to read the x- and y-axes of the joystick, and also polls two digital inputs to read the status of the joystick's two buttons.

It sends a 32-bit hexadecimal message when any change in joystick status is detected. This message currently is configured as follows (MSB first):

18 bits | 1 bit | 1 bit | 6 bits | 6 bits
--------|-------|-------|--------|--------
ms since last message | button 1 | button 2 | x value | y value

The included Python script decodes the message and uses [PyUserInput](https://github.com/SavinaRoja/PyUserInput) to implement basic mouse control (unfinished).

Eventually the idea is to include USB connectivity to the hardware portion and make the joystick appear as a USB HID mouse.
