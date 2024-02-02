Linux /Unix Users
==========================


#. Go to **Applications**->\ **Utilities**, find the **Terminal**, and open
it.

    .. image:: img/image21.png
        :align: center

#. Check if your Raspberry Pi is on the same network by type in ``ping <hostname>.local``. 

    .. code-block::

        ping raspberrypi.local

    .. image:: img/mac-ping.png
        :width: 550
        :align: center

    As shown above, you can see the Raspberry Pi's IP address after it has been connected to the network.

    * If terminal prompts ``Ping request could not find host pi.local. Please check the name and try again.``. Please follow the prompts to make sure the hostname you fill in is correct.
    * Still can't get the IP? Check your network or WiFi configuration on the Raspberry Pi.


#. Type in ``ssh <username>@<hostname>.local`` (or ``ssh <username>@<IP address>``).

    .. code-block::

        ssh pi@raspberrypi.local

    .. note::

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



#. We now get the Raspberry Pi connected and are ready to go to the nextstep.

    .. image:: img/mac-ssh-terminal.png
        :width: 550
        :align: center