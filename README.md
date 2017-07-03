# Coffee Collector

Pixel Fusion coffee collector, the ultrasonic distance sensor measures how full the collector is. 
Based on the level it gives updates on Slack and real time information on the led screen.

## Hardware
* Raspberry pi Zero W
* Adafruit SSD1306 128*32 led screen
* HC-SR04 ultrasonic distance ranging module

## Wiring
![Wiring digram](/images/setup_bb_zero.png?raw=true "Wiring digram")

Color layout:
##### SENSOR
* blue=5V
* purple=GPIO14 | trig
* grey=Ground
* white=GPIO23 | echo

##### LED-SCREEN
* green=SDA
* yellow=SCL
* orange=Ground
* red=3.3V

## Configure Raspberry Pi
* Follow the installation process described on [Raspberry pi install](https://www.raspberrypi.org/documentation/installation/installing-images/)
* Add an empty file `ssh` on the boot partition (so we can ssh into the pi)
* Add an `wpa_supplicant.conf` file to the boot partition (this will load the wifi config)
Example config:
```
network={
    ssid="wifi_ssid"
    psk="wifi_password"
}
```
* Boot the pi and scan your network, SSH into you pi with the default password and username 
* After you logged in you need to update the password with `passwd`
* Make sure git is installed on your pi, otherwise run `sudo apt-get install git`
* Run the following command to setup the code, `mkdir ~/scripts && cd ~/scripts && git clone https://github.com/pixelfusion/coffee-collector-messenger.git`
* Make sure pip and essential tools are installed, otherwise run `sudo apt-get install build-essential python-dev python-pip`
* Make sure you have python images installed, otherwise run `sudo apt-get install python-imaging python-smbus`
* Install requirements for the python script `pip install -r requirements.txt`
* Enable I2C for the display `sudo apt-get install -y i2c-tools`
* Setup I2C, `sudo vi /etc/modules` add:
```
i2c-bcm2708 
i2c-dev
```
* Also edit `/boot/config.txt` and  add or uncomment:
```
dtparam=i2c1=on
dtparam=i2c_arm=on
```
* Reboot the pi and verify that I2C is setup with `sudo i2cdetect -y 1`

Reference for the I2C setup [Adafruit Raspberry pi configuring i2c](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)

## Booting the script
* Setup your `.env` file, see the `.env.example` for reference
* To auto start the script on boot, you can use a cronjob:
```
@reboot echo "$(date) $(ls -1 | wc -l)" >> ~/scripts/log-cc.txt
@reboot python ~/scripts/coffee-collector-messenger/script.py >> ~/scripts/log-cc.txt 2>&1
```
* Reboot the pi, and the script should run now
* You can also review the logs, if you have any issues `tail -f ~/scripts/log-cc.txt`


## Slack notification levels
* percentage is calculated with the height of the can + 10% safety margin.
* [Formula helper](https://github.com/pixelfusion/coffee-collector-messenger/blob/master/Services/helpers.py#L10)

| Status | CM's left | Color | Emoticon | Percentage of water | Special
|--|--|--|--|--|--|
| A | `>32` | Green | :grinning: | 0% - 30% | x |
| B | `> 24 and <=32` | Blue | :slightly_smiling_face: | 30% - 50% | x |
| C | `> 16 and <=24 ` | Orange | :cold_sweat: | 50% - 70% | x |
| D | `>16` | Red | :scream: | 70% - 100% | Tag 3 slack users |

## Gotchas
* Make the sensor align perfectly downwards, otherwise you get diverse readings
