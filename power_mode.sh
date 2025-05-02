#!/bin/bash
# Toggle power saving mode on Raspberry Pi OS Lite
# Usage: sudo ./power_mode.sh --on   # Enable power saving
#        sudo ./power_mode.sh --off  # Restore normal settings

CONFIG_FILE="/boot/config.txt"
CMDLINE_FILE="/boot/cmdline.txt"

enable_power_saving() {
    echo "Applying power saving mode..."

    # Underclock CPU and reduce voltage
    sudo sed -i '/^arm_freq=/d;/^core_freq=/d;/^sdram_freq=/d;/^over_voltage=/d' "$CONFIG_FILE"
    echo -e "\narm_freq=600\ncore_freq=200\nsdram_freq=300\nover_voltage=-4" | sudo tee -a "$CONFIG_FILE" > /dev/null

    # Disable HDMI — only works if vc4-kms is disabled or replaced
    sudo sed -i '/^dtoverlay=vc4-/d' "$CONFIG_FILE"
    echo "dtoverlay=disable-vc4" | sudo tee -a "$CONFIG_FILE" > /dev/null  # Disable GPU
    echo "gpu_mem=16" | sudo tee -a "$CONFIG_FILE" > /dev/null            # Minimize GPU memory

    # Disable LEDs if present
    [ -e /sys/class/leds/led0/brightness ] && echo 0 | sudo tee /sys/class/leds/led0/brightness
    [ -e /sys/class/leds/led1/brightness ] && echo 0 | sudo tee /sys/class/leds/led1/brightness

    # Disable Bluetooth only
    sudo rfkill block bluetooth  # Disable Bluetooth only
    sudo sed -i '/^dtoverlay=disable-bt/d' "$CONFIG_FILE"
    echo "dtoverlay=disable-bt" | sudo tee -a "$CONFIG_FILE" > /dev/null

    # Disable unused services
    sudo systemctl disable avahi-daemon  # Disable Avahi mDNS
    sudo systemctl disable triggerhappy  # Disable triggerhappy
    sudo systemctl disable bluetooth     # Disable Bluetooth service

    # Enable USB autosuspend
    if ! grep -q "usbcore.autosuspend=1" "$CMDLINE_FILE"; then
        sudo sed -i 's/\(.*\)/\1 usbcore.autosuspend=1/' "$CMDLINE_FILE"  # Add USB autosuspend
    fi

    echo "Power saving enabled (Wi-Fi retained). Please reboot to apply changes."
}

disable_power_saving() {
    echo "Reverting to normal power settings..."

    # Remove underclock settings
    sudo sed -i '/^arm_freq=/d;/^core_freq=/d;/^sdram_freq=/d;/^over_voltage=/d' "$CONFIG_FILE"
    sudo sed -i '/^dtoverlay=disable-vc4/d;/^gpu_mem=/d' "$CONFIG_FILE"

    # Enable LEDs if present
    [ -e /sys/class/leds/led0/brightness ] && echo 1 | sudo tee /sys/class/leds/led0/brightness
    [ -e /sys/class/leds/led1/brightness ] && echo 1 | sudo tee /sys/class/leds/led1/brightness

    # Re-enable Bluetooth
    sudo rfkill unblock bluetooth
    sudo sed -i '/^dtoverlay=disable-bt/d' "$CONFIG_FILE"

    # Re-enable services
    sudo systemctl enable avahi-daemon
    sudo systemctl enable triggerhappy
    sudo systemctl enable bluetooth

    # Remove USB autosuspend
    sudo sed -i 's/ usbcore.autosuspend=1//' "$CMDLINE_FILE"

    echo "Normal settings restored. Please reboot to apply changes."
}

case "$1" in
    --on)
        enable_power_saving
        ;;
    --off)
        disable_power_saving
        ;;
    *)
        echo "Usage: sudo $0 --on | --off"
        exit 1
        ;;
esac
