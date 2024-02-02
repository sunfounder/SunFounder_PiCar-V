Enable I2C Interface(Important)
========================================

Here we are using the Raspberry Pi's I2C interfaces, but by default they are disabled, so we need to enable them first.

#. Input the following command:

    .. raw:: html

        <run></run>

    .. code-block:: 

        sudo raspi-config

#. Choose **Interfacing Options** by press the down arrow key on your keyboard, then press the **Enter** key.

    .. image:: img/image282.png
        :align: center

#. Then **I2C**.

    .. image:: img/image283.png
        :align: center

#. Use the arrow keys on the keyboard to select **<Yes>** -> **<OK>** to complete the setup of the I2C.

    .. image:: img/image284.png
        :align: center

#. After you select **<Finish>**, a pop-up will remind you that you need to reboot for the settings to take effect, select **<Yes>**.

    .. image:: img/camera_enable2.png
        :align: center