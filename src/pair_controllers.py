# Standalone script to pair bluetooth controllers with the name "Pro Controller" to this device.

import asyncio
import subprocess
from bleak import BleakScanner, BleakClient


async def find_devices(device_name):
    print("Scanning for Bluetooth devices...")
    devices = await BleakScanner.discover()
    
    print("Found devices:")
    for device in devices:
        print(f"  {device.name} ({device.address})")
    return [device for device in devices if device_name in device.name]


def pair_device(device_mac):
    """Pair the device using bluetoothctl."""
    print(f"Pairing with {device_mac}...")
    subprocess.run(["bluetoothctl", "pair", device_mac], capture_output=True, text=True)
    subprocess.run(["bluetoothctl", "trust", device_mac], capture_output=True, text=True)


async def connect_device(device_mac):
    """Attempt to connect to a Bluetooth device."""
    print(f"Connecting to {device_mac}...")
    
    async with BleakClient(device_mac) as client:
        if client.is_connected:
            print(f"Connected successfully to {device_mac}!")
        else:
            print(f"Failed to connect to {device_mac}.")


async def main():
    device_name = "Pro Controller"
    devices = await find_devices(device_name)
    
    for device in devices:
        pair_device(device.address)
        await connect_device(device.address)
    else:
        print(f"No new devices found with name '{device_name}'.")

if __name__ == "__main__":
    asyncio.run(main())