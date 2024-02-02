.. _filezilla:

Filezilla Software
==========================

.. image:: img/filezilla_icon.png

The File Transfer Protocol (FTP) is a standard communication protocol used for the transfer of computer files from a server to a client on a computer network.

Filezilla is an open source software that not only supports FTP, but also FTP over TLS (FTPS) and SFTP. We can use Filezilla to upload local files (such as pictures and audio, etc.) to the Raspberry Pi, or download files from the Raspberry Pi to the local.

**Step 1**: Download Filezilla.

Download the client from `Filezilla’s official website <https://filezilla-project.org/>`_, Filezilla has a very good tutorial, please refer to: `Documentation - Filezilla <https://wiki.filezilla-project.org/Documentation>`_.

**Step 2**: Connect to Raspberry Pi

After a quick install open it up and now `connect it to an FTP server <https://wiki.filezilla-project.org/Using#Connecting_to_an_FTP_server>`_. It has 3 ways to connect, here we use the **Quick Connect** bar. Enter the **hostname/IP**, **username**, **password** and **port (22)**, then click **Quick Connect** or press **Enter** to connect to the server.

.. image:: img/filezilla_connect.png

.. note::

    Quick Connect is a good way to test your login information. If you want to create a permanent entry, you can select **File**-> **Copy Current Connection to Site Manager** after a successful Quick Connect, enter the name and click **OK**. Next time you will be able to connect by selecting the previously saved site inside **File** -> **Site Manager**.
    
    .. image:: img/ftp_site.png

**Step 3**: Upload/download files.

You can upload local files to Raspberry Pi by dragging and dropping them, or download the files inside Raspberry Pi
files locally.

.. image:: img/upload_ftp.png
