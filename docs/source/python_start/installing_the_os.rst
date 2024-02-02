Installing the OS
=======================

**Required Components**

* Raspberry Pi 4B/Zero 2 w/3B 3B+/2B/Zero W
* 1 x Personal Computer
* 1 x Micro SD card 

**Steps**


#. Go to the Raspberry Pi software download page: `Raspberry Pi Imager <https://www.raspberrypi.org/software/>`_. Select the Imager version for your operating system. After downloading, open the file to start the installation.

    .. image:: img/os_install_imager.png


#. Upon launching the installer, your OS might display a security warning. For instance, Windows may show a caution message. If this occurs, select **More info** and then **Run anyway**. Follow the on-screen instructions to install the Raspberry Pi Imager.

    .. image:: img/os_info.png


#. Insert your SD card into the computer or laptop SD card slot.

#. Open the Raspberry Pi Imager application either by clicking its icon or executing ``rpi-imager`` in your terminal.

    .. image:: img/os_open_imager.png

#. Click **CHOOSE DEVICE** and select your specific Raspberry Pi model from the list (Note: Raspberry Pi 5 is not applicable).

    .. image:: img/os_choose_device.png

#. Select **CHOOSE OS** and then choose **Raspberry Pi OS (Legacy)**.

    .. warning::
        * Please do not install the **Bookworm** version as the speaker will not work.
        * You need to install the **Raspberry Pi OS (Legacy)** version - **Debian Bullseye**.

    .. image:: img/os_choose_os.png


#. Click **Choose Storage** and pick the correct storage device for the installation.

    .. note::

        Be sure to select the correct device, especially if multiple storage devices are connected. Disconnect others if you're unsure.

    .. image:: img/os_choose_sd.png

#. Press **NEXT** and select **EDIT SETTINGS** to customize your OS settings.

    .. image:: img/os_enter_setting.png

#. Set your Raspberry Pi's **hostname**.

    .. note::

        The hostname is what your Raspberry Pi uses to identify itself on the network. You can connect to your Pi using `<hostname>.local` or `<hostname>.lan`.

    .. image:: img/os_set_hostname.png

#. Create a **Username** and **Password** for the Raspberry Pi's administrator account.

    .. note::

        Setting a unique username and password is crucial for security, as the Raspberry Pi does not have a default password.

    .. image:: img/os_set_username.png

#. Set up wireless LAN by inputting your network's **SSID** and **Password**.

    .. note::

        ``Wireless LAN country`` should be set the two-letter `ISO/IEC alpha2 code <https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements>`_ for the country in which you are using your Raspberry Pi.

    .. image:: img/os_set_wifi.png


#. Click **SERVICES** and enable **SSH** for password-based remote access. Remember to click **Save**.

    .. image:: img/os_enable_ssh.png

#. Confirm your choices by clicking **Yes**.

    .. image:: img/os_click_yes.png

#. If your SD card has existing files, back them up to avoid data loss. Click **Yes** to proceed if no backup is necessary.

    .. image:: img/os_continue.png

#. Wait as the OS is written to the SD card. Once completed, a confirmation window will appear.

    .. image:: img/os_finish.png
        :align: center