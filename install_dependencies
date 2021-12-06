#!/bin/bash
#Installation

##Tested on:

#- Raspbian (RaspberryPi - think of those possibilities)

#```

# All of these commands are run from the base folder (SunFounder_Smart_Video_Car_Kit_V2.0_for_Raspberry_Pi), wherever you clone it to
repo_dir=`pwd`

is_installed_django=False
is_installed_python_smbus=False
is_installed_python_opencv=False
is_installed_libjpeg8_dev=False

if [ "$(whoami)" != "root" ] ; then
    echo -e "You must run this script as root."
    exit
fi

sudo apt-get update
#sudo apt-get upgrade -y

function if_continue(){
    while :; do
        echo  -e "(yes/no) \c"
        read input_item
        if [ $input_item = "yes" ]; then
            break
        elif [ $input_item = "no" ]; then
            return 0
        else
            echo -e "Input error, please try again."
        fi
    done
    return 1
}

function end(){
    print_result
    echo -e "Exiting..."
    exit
}

function print_result(){
    echo -e "Installation result:"
    echo -e "django   \c"
    if $is_installed_django; then
        echo -e "Success"
    else
        echo -e "Failed"
    fi
    echo -e "python-smbus  \c"
    if $is_installed_python_smbus; then
        echo -e "Success"
    else
        echo -e "Failed"
    fi
    echo -e "python-opencv  \c"
    if $is_installed_python_opencv; then
        echo -e "Success"
    else
        echo -e "Failed"
    fi
#     echo -e "libjpeg8-dev  \c"
#     if $is_installed_libjpeg8_dev; then
#         echo -e "Success"
#     else
#         echo -e "Failed"
#     fi
}

###################################
# install python-pip django i2c-tools python-smbus python-opencv runtime #
###################################
echo -e "\nInstalling django \n"
if sudo pip3 install django==2.0 ; then
    echo -e "    Successfully installed django runtime \n"
    is_installed_django=true
else
    echo -e "    Failed to installed django."
    echo -e "    Do you want to skip this? \c"
    if_continue
    if [ $? = 1 ] ; then
        echo -e "    Skipped django installation."
    else
        end
    fi
fi

echo -e "\nInstalling python3-smbus and git\n"
if sudo apt-get install python3-smbus git -y; then
    echo -e "    Successfully installed python-smbus and git\n"
    is_installed_python_smbus=true
else
    echo -e "    Failed to installed python-smbus and git\n"
    echo -e "    Do you want to skip this? \c"
    if_continue
    if [ $? = 1 ] ; then
        echo -e "    Skipped python-smbus and git installation."
    else
        end
    fi
fi

echo -e "\nInstalling python3-opencv \n"
if sudo apt-get install python3-opencv -y; then
    echo -e "    Successfully installed python-opencv \n"
    is_installed_python_opencv=true
else
    echo -e "    Failed to installed python-opencv \n"
    echo -e "    Do you want to skip this? \c"
    if_continue
    if [ $? = 1 ] ; then
        echo -e "    Skipped python-opencv installation."
    else
        end
    fi
fi

# echo -e "\nInstalling libjpeg8-dev \n"
# if sudo apt-get install libjpeg8-dev -y; then
#     echo -e "    Successfully installed libjpeg8-dev \n"
#     is_installed_libjpeg8_dev=true
# else
#     echo -e "    Failed to installed libjpeg8-dev \n"
#     echo -e "    Do you want to skip this? \c"
#     if_continue
#     if [ $? = 1 ] ; then
#         echo -e "    Skipped libjpeg8-dev installation."
#     else
#         end
#     fi
# fi

###################################
# Install RPi Car V2 Module
###################################

echo -e "Cloning repo \n"
cd ../
git clone --recursive https://github.com/sunfounder/SunFounder_PiCar.git
cd SunFounder_PiCar
echo -e "    Installing PiCar module \n"
sudo python setup.py install
sudo python3 setup.py install
cd $repo_dir
echo -e "complete\n"

###################################
# Copy MJPG-Streamer to an Alternate Location #
###################################
#
echo -e "Copy MJPG-Streamer to an Alternate Location. \n"
sudo cp $repo_dir/mjpg-streamer/mjpg_streamer /usr/local/bin
sudo cp $repo_dir/mjpg-streamer/output_http.so mjpg-streamer/input_file.so mjpg-streamer/input_uvc.so /usr/local/lib/
sudo cp -R $repo_dir/mjpg-streamer/www /usr/local/www
sudo chmod +x /usr/local/bin/mjpg_streamer
echo -e "complete\n"

###################################
# Export Paths #
###################################
#
#echo -e "Export paths. \n"
#echo -e export LD_LIBRARY_PATH=/usr/local/lib/ >> ~/.bashrc
#echo -e export LD_LIBRARY_PATH=/usr/local/lib/ >> ~/.profile
#source ~/.bashrc
#echo -e "complete. \n"

###################################
# Enable I2C1 #
###################################
# Add lines to /boot/config.txt
echo -e "Enalbe I2C \n"
egrep -v "^#|^$" /boot/config.txt > config.txt.temp  # pick up all uncomment configrations
if grep -q 'dtparam=i2c_arm=on' config.txt.temp; then  # whether i2c_arm in uncomment configrations or not
    echo -e '    Seem i2c_arm parameter already set, skip this step \n'
else
    echo -e '    dtparam=i2c_arm=on \n' >> /boot/config.txt
fi
rm config.txt.temp
echo -e "complete\n"

print_result

echo -e "The stuff you have change may need reboot to take effect."
echo -e "Do you want to reboot immediately? \c"
if_continue
if [ $? = 1 ]; then
    echo -e "Rebooting..."
    sudo reboot
else
    echo -e "Exiting..."
    exit
fi
