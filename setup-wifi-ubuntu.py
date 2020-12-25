#!/usr/bin/python3
from getpass import getpass
from pathlib import Path
from typing import Dict
from yaml import safe_dump

def setup_config(ssid: str, password: str) -> Dict[str, str]:
    '''Create a basic Netplan configuration data structure

    Args:
        ssid: The name of the SSID
        password: The password for the SSID

    Returns:
        A Netplan configuration data structure
    '''
    netplan_config = {
        'network': {
            'ethernets': {
                'eth0': {
                    'dhcp4': True,
                    'optional': True
                }
            },
            'version': 2,
            'wifis': {
                'wlan0': {
                    'optional': True,
                    'access-points': {
                        ssid: {
                            'password': password
                        }
                    },
                    'dhcp4': True
                }
            }
        }
    }

    return netplan_config


def check_path() -> bool:
    netplan_path = Path('/etc/netplan/')
    if netplan_path.exists() is False:
        


if __name__ == '__main__':
    '''No sanity checking because YOLO'''
    ssid = input('WiFi SSID Name: ')
    password = getpass('WiFi Password: ')

    config = setup_config(ssid=ssid, password=password)
