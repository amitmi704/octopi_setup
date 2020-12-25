#/usr/bin/python3
from getpass import getpass
from pathlib import Path
from subprocess import run

if __name__ == '__main__':
    wifi_conf = Path('/boot/wpa_supplicant.conf')
    conf_file = ''
    if wifi_conf.exists() is False:
        print(f'WiFi config file does not exist: {wifi_conf}')
    else:
        try:
            with wifi_conf.open() as file:
                conf_file = file.read()
        except PermissionError as e:
            print(f'Re-run with root permissions: `sudo ./{__file__}`') 
            raise e

    ssid = input('WiFi SSID: ')
    psk = getpass('WiFi PSK: ')
    if len(psk) < 8 or 63 < len(psk):
        raise ValueError(f'PSK length is too long [8,63]: {len(psk)}')

    wpa_supplicant_conf = ('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n'
                           'update_config=1\n'
                           'country=US')
    wpa_passphrase = run(['wpa_passphrase', ssid, psk], capture_output=True)
    wpa_passphrase.check_returncode()
    wpa_psk_conf = wpa_passphrase.stdout.decode('utf-8').split('\n')
    wpa_psk_conf.pop(2)
    wpa_psk_conf = '\n'.join(wpa_psk_conf)

    wpa_supplicant_conf = '\n'.join([wpa_supplicant_conf, wpa_psk_conf])

    if wpa_supplicant_conf != conf_file:
        print(f'Writing out new configuration file to {wifi_conf}')
        try:
            with wifi_conf.open(mode='w') as file:
                file.write(wpa_supplicant_conf)
        except PermissionError as e:
            print(f'Re-run with root permissions: `sudo ./{__file__}`')
            raise e

        service = run(['systemctl', 'restart', 'raspberrypi-net-mods.service'], capture_output=True)
        service.check_returncode()

        print('Performing WPA Supplicant configuration update...')
        wpa_reconfig = run(['wpa_cli', '-i', 'wlan0', 'reconfigure'], capture_output=True)
        if wpa_reconfig.returncode != 0:
          raise RuntimeError(f'Unexpected exit code received, output: {wpa_reconfig.returncode}, {wpa_reconfig.stdout.decode("utf-8")}')
        
        print('Re-configuration succeeded!')
    else:
        print('No re-configuration needed!')
