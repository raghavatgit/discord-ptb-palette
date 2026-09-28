import subprocess
import ctypes

def refresh_icon_cache():
    try:
        subprocess.run(["ie4uinit.exe", "-show"], capture_output=True)
    except Exception as e:
        print(f"  Note: ie4uinit: {e}")
    try:
        # SHCNE_ASSOCCHANGED = 0x08000000, SHCNF_IDLIST = 0
        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0, None, None)
        print("  Windows icon cache notified successfully.")
    except Exception as e:
        print(f"  Note: SHChangeNotify: {e}")
