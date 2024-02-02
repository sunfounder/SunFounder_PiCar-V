Windows Users
=======================

Login Raspberry Pi Remotely
-----------------------------

If you are using win10, you can use follow way to login Raspberry Pi remotely.

#. Type ``powershell`` in the search box of your Windows desktop, right click on the ``Windows PowerShell``, and select ``Run as administrator`` from the menu that appears.

    .. image:: img/powershell_ssh.png
        :align: center

#. Then, check the IP address of your Raspberry Pi by typing in ``ping -4 <hostname>.local``. 

    .. code-block::

        ping -4 raspberrypi.local

    .. image:: img/sp221221_145225.png
        :width: 550
        :align: center

    As shown above, you can see the Raspberry Pi's IP address after it has been connected to the network.

    * If terminal prompts ``Ping request could not find host pi.local. Please check the name and try again.``. Please follow the prompts to make sure the hostname you fill in is correct.
    * Still can't get the IP? Check your network or WiFi configuration on the Raspberry Pi.


#. At this point you will be able to log in to your Raspberry Pi using the ``ssh <username>@<hostname>.local`` (or ``ssh <username>@<IP address>``).

    .. code-block::

        ssh pi@raspberrypi.local

    .. warning::

        If a prompt appears ``The term 'ssh' is not recognized as the name of a cmdlet...``.
        
        It means your system is too old and does not have ssh tools pre-installed, you need to manually :ref:`openssh_powershell`.
        
        Or use a third party tool like :ref:`login_windows`.


#. The following message will be displayed only when you log in for the first time, so enter ``yes``.

    .. code-block::

        The authenticity of host 'raspberrypi.local (2400:2410:2101:5800:635b:f0b6:2662:8cba)' can't be established.
        ED25519 key fingerprint is SHA256:oo7x3ZSgAo032wD1tE8eW0fFM/kmewIvRwkBys6XRwg.
        This key is not known by any other names
        Are you sure you want to continue connecting (yes/no/[fingerprint])?


#. Input the password you set before. (Mine is ``raspberry``.)

    .. note::
        When you input the password, the characters do not display on
        window accordingly, which is normal. What you need is to input the
        correct password.

#. We now get the Raspberry Pi connected and are ready to go to the next step.

    .. image:: img/sp221221_140628.png
        :width: 550
        :align: center

.. _remote_desktop:

Remote Desktop
------------------

If you're not satisfied with using the command window to access your Raspberry Pi, you can also use the remote desktop feature to easily manage files on your Raspberry Pi using a GUI.

Here we use `VNC® Viewer <https://www.realvnc.com/en/connect/download/viewer/>`_.

**Enable VNC service**

The VNC service has been installed in the system. By default, VNC is
disabled. You need to enable it in config.

#. Input the following command:

    .. raw:: html

        <run></run>

    .. code-block:: 

        sudo raspi-config

    .. image:: img/image287.png
        :align: center

#. Choose **3** **Interfacing Options** by press the down arrow key on your keyboard, then press the **Enter** key.

    .. image:: img/image282.png
        :align: center

#. Then **VNC**. 

    .. image:: img/image288.png
        :align: center

#. Use the arrow keys on the keyboard to select **<Yes>** -> **<OK>** -> **<Finish>** to complete the setup.

    .. image:: img/mac_vnc8.png
        :align: center

**Login to VNC**

#. You need to download and install the `VNC Viewer <https://www.realvnc.com/en/connect/download/viewer/>`_ on personal computer.

#.  Open it once the installation is complete. Then, enter the host name or IP address and press Enter.

    .. image:: img/vnc_viewer1.png
        :align: center

#. After entering your Raspberry Pi name and password, click **OK**.

    .. image:: img/vnc_viewer2.png
        :align: center

#. Now you can see the desktop of the Raspberry Pi.

    .. image:: img/image294.png
        :align: center
