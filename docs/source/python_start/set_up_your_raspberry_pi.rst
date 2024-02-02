Set up Your Raspberry Pi
============================
Power Supply for Raspberry Pi (Important)
--------------------------------------------------

#. Insert the SD card set up with Raspberry Pi OS into the microSD card slot located on the underside of the Raspberry Pi.

    .. .. image:: img/insert_sd_card.png
    ..     :width: 500
    ..     :align: center

#. Following the assembly instructions, insert the battery cable and turn on the power switch. Next, insert the USB cable to Raspberry Pi. 
    .. image:: img/BTR_power_in.png

    .. .. image:: img/Z_BTR.JPG
    ..     :width: 800
    ..     :align: center

    .. .. note::

    ..     It is recommended to leave the USB-C cable plugged in, as the subsequent software setup process can take a considerable amount of time.


If You Have a Screen
-------------------------

.. note:: The Raspberry Pi ZERO installed on the Robot is not easy to connect to the screen, please use the method without a screen to set it up.


If you have a screen, it will be easy for you to operate on the
Raspberry Pi.

**Required Components**

* Raspberry Pi 4B/3B 3B+/2B
* 1 * Power Adapter
* 1 * Micro SD card
* 1 * Screen Power Adapter
* 1 * HDMI cable
* 1 * Screen
* 1 * Mouse
* 1 * Keyboard

#. Plug in the Mouse and Keyboard.

#. Connect the screen to Raspberry Pi's HDMI port and make sure your screen is plugged into a wall socket and switched on.

    .. note::

        If you use a Raspberry Pi 4, you need to connect the screen to the HDMI0 (nearest the power in port).

#. Use the power adapter to power the Raspberry Pi. After a few seconds, the Raspberry Pi OS desktop will be displayed.

    .. image:: img/image20.png
        :align: center

If You Have No Screen
--------------------------

If you don't have a monitor, you can remotely log into your Raspberry Pi.

**Required Components**

* * Raspberry Pi 4B/Zero 2 w/3B 3B+/2B/Zero W  
* 1 * Power Adapter
* 1 * Micro SD card

You can apply the SSH command to open the Raspberry Pi's Bash shell. Bash is the standard default shell for Linux. The shell itself is a command (instruction) when the user uses Unix/Linux. Most of what you need to do can be done through the shell.

If you're not satisfied with using the command window to access your Raspberry Pi, you can also use the remote desktop feature to easily manage files on your Raspberry Pi using a GUI.

See below for detailed tutorials for each system.


.. toctree::

    remote_macosx
    remote_windows
    remote_linux

