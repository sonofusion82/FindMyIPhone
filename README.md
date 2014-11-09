FindMyIPhone
============

Raspberry PI FindMyIPhone is simple script that will login to iCloud and trigger Find My IPhone feature to cause your iDevice to play a sound.

Currently, it uses GPIO 23 as LED output and GPIO 24 as button input (active low). Perhaps we can make it configurable with the json file in future.

To launch, just start the script and provide it with a config file containing your iCloud usename and password, see exampleConfig.json

    sudo ./FindMyIPhone.py exampleConfig.json

Note that because it depends on RPi.GPIO module, you will need to run it as a root user to have access to the GPIOs

You can also set it to launch during system boot by creating an init script at /etc/init.d/FindMyIPhone. Example:


    #! /bin/sh
    # /etc/init.d/FindMyIPhone

    ### BEGIN INIT INFO
    # Provides:          FindMyIPhone
    # Required-Start:    $all
    # Required-Stop:     $local_fs $network
    # Default-Start:     2 3 4 5
    # Default-Stop:      0 1 6
    # Short-Description: Start FindMyIPhone at boot time
    # Description:       Launch FindMyIPhone during system init
    ### END INIT INFO

    # Carry out specific functions when asked to by the system
    case "$1" in
    start)
        nice -n1 /home/pi/FindMyIPhone/FindMyIPhone.py /home/pi/FindMyIPhone/FindMyIPhone.json
        ;;
    stop)
        killall FindMyIPhone
        ;;
    *)
        echo "Usage: /etc/init.d/FindMyIPhone {start|stop}"
        exit 1
        ;;
    esac

    exit 0

After adding the init script, update system init scripts with:

    sudo update-rc.d FindMyIPhone defaults

Dependencies:
- python-daemon https://pypi.python.org/pypi/python-daemon/
- RPi.GPIO https://pypi.python.org/pypi/RPi.GPIO
- pyicloud https://pypi.python.org/pypi/pyicloud/0.5.2


