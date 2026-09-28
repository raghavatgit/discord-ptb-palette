import os
import glob

def get_base_dir():
    base = os.path.expandvars(r"%LOCALAPPDATA%\DiscordPTB")
    if not os.path.isdir(base):
        raise RuntimeError(f"DiscordPTB directory not found at: {base}")
    return base

def get_active_app_dir():
    base = get_base_dir()
    app_dirs = sorted(
        [d for d in os.listdir(base) if d.startswith("app-") and os.path.isdir(os.path.join(base, d))],
        reverse=True
    )
    if not app_dirs:
        raise RuntimeError("No app-* directory found in DiscordPTB base folder")
    return os.path.join(base, app_dirs[0])

def get_tray_pngs(app_dir=None):
    if not app_dir:
        app_dir = get_active_app_dir()
    tray_glob = os.path.join(
        app_dir, "modules", "discord_desktop_core-*",
        "discord_desktop_core", "app", "images",
        "systemtray", "win32", "*.png"
    )
    return glob.glob(tray_glob)

def get_source_ico():
    base = get_base_dir()
    src_ico = os.path.join(base, "app.ico")
    if not os.path.isfile(src_ico):
        raise RuntimeError(f"Source app.ico not found at: {src_ico}")
    return src_ico
