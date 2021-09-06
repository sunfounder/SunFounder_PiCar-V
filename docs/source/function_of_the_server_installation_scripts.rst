Appendix 1: Function of the Server Installation Scripts
=======================================================

You may have a question: What do the installation scripts do when we
install the server on the Raspberry Pi by them? So here let's check the
detailed steps.

1. Install pip.

.. raw:: html

    <run></run>

.. code-block::

    sudo apt-get install python-pip

2. Use pip to install django.

.. raw:: html

    <run></run>

.. code-block::

    sudo pip install django

3. Install i2c-tools and python-smbus.

.. raw:: html

    <run></run>

.. code-block::

    sudo pip3 install smbus2

4. Install PiCar drivers.

.. raw:: html

    <run></run>

.. code-block::

    cd ~/
    git clone -–recursive https://github.com/sunfounder/SunFounder_PiCar.git
    cd SunFounder_PiCar
    sudo python setup.py install

5. Download source code.

.. raw:: html

    <run></run>

.. code-block::

    cd ~/
    git clone https://github.com/sunfounder/SunFounder_PiCar-V -b V3.0

6. Copy the MJPG-Streamer file to system directory.

.. raw:: html

    <run></run>

.. code-block::

    cd ~/SunFounder_PiCar-V
    sudo cp mjpg-streamer/mjpg_streamer /usr/local/bin
    sudo cp mjpg-streamer/output_http.so /usr/local/lib/
    sudo cp mjpg-streamer/input_file.so /usr/local/lib/
    sudo cp mjpg-streamer/input_uvc.so /usr/local/lib/
    sudo cp -R mjpg-streamer/www /usr/local/www

7. Export paths.

.. raw:: html

    <run></run>

.. code-block::

    export LD_LIBRARY_PATH=/usr/local/lib/ >> ~/.bashrc
    export LD_LIBRARY_PATH=/usr/local/lib/ >> ~/.profile
    source ~/.bashrc

8. Enable I2C1.

Edit the file /boot/config.txt:

.. raw:: html

    <run></run>

.. code-block::

    sudo nano /boot/config.txt 

Add the line in the end:

.. raw:: html

    <run></run>

.. code-block::

    dtparam=i2c_arm=ons

9. Reboot.

.. raw:: html

    <run></run>

.. code-block::

    sudo reboot