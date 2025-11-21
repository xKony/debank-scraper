import time
from nordvpn_switcher_pro import VpnSwitcher
import subprocess
from nordvpn_switcher_pro.exceptions import NordVpnConnectionError


def vpn_rotation():
    switcher = VpnSwitcher()
    switcher.start_session()
    try:
        switcher.rotate()
        print("[VPN] Rotation complete.\n")
    except NordVpnConnectionError as e:
        print(f"[ERROR] {e}")
        handle_critical_error(switcher)


def handle_critical_error(switcher: VpnSwitcher):
    print("[VPN] Critical error detected. Restarting NordVPN...")
    subprocess.run("taskkill /F /IM nordvpn.exe /T", shell=True)
    subprocess.run("taskkill /F /IM nordvpn.exe /T", shell=True)
    time.sleep(5)
    try:
        switcher.start_session()
        time.sleep(15)
        switcher.rotate()
        print("[VPN] Reconnected successfully after error.")
    except NordVpnConnectionError as e:
        print(f"[VPN] Retry failed: {e}. Waiting 15s before next attempt...")
        time.sleep(15)
        handle_critical_error()
