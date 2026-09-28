#!/usr/bin/env python3
"""
DiscordPTB Theme Manager
=========================
Feature-based theme switcher for DiscordPTB.

Usage:
  python apply_theme.py [green|red|default]
"""

import os
import sys
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.discord_paths import get_active_app_dir, get_tray_pngs, get_source_ico
from core.recolor_engine import build_multiscale_ico, recolor_tray_pngs, THEME_SPECS
from core.shortcut_manager import patch_shortcuts, create_one_click_runner
from core.cache import refresh_icon_cache

def apply(theme="green"):
    theme = theme.lower().strip()
    if theme not in THEME_SPECS:
        print(f"Unknown theme: {theme}. Choose from: {list(THEME_SPECS.keys())}")
        sys.exit(1)

    spec = THEME_SPECS[theme]
    print(f"=== Applying DiscordPTB Theme: {spec['name']} ({theme}) ===")

    # 1. Locate paths
    app_dir = get_active_app_dir()
    src_ico = get_source_ico()
    tray_files = get_tray_pngs(app_dir)
    print(f"  Active app dir : {app_dir}")
    print(f"  Tray icons     : {len(tray_files)} found")

    # 2. Build multi-resolution icon in themes/<theme>/icon.ico
    theme_ico = os.path.join(BASE_DIR, "themes", theme, "icon.ico")
    build_multiscale_ico(src_ico, theme_ico, theme)
    print(f"  Theme icon saved: {theme_ico}")

    # Also update root-level icon copy for compatibility
    if theme == "green":
        root_ico = os.path.join(BASE_DIR, "discord_ptb_green.ico")
        shutil.copy2(theme_ico, root_ico)
    elif theme == "red":
        root_ico = os.path.join(BASE_DIR, "discord_ptb_red.ico")
        shutil.copy2(theme_ico, root_ico)

    # Copy to active app-* directory (window icon fallback)
    try:
        app_ico_target = os.path.join(app_dir, "app.ico")
        shutil.copy2(theme_ico, app_ico_target)
        print(f"  Updated app-dir app.ico: {app_ico_target}")
    except Exception as e:
        print(f"  Note: Could not update app-dir app.ico: {e}")

    # 3. Recolor tray PNGs
    ok, fail = recolor_tray_pngs(tray_files, theme)
    print(f"  Tray icons processed: {ok} succeeded, {fail} failed")

    # 4. Patch Start Menu and Desktop shortcuts
    patch_shortcuts(theme_ico)

    # 5. Ensure Desktop and shortcuts/ one-click runners
    runner_script = os.path.join(BASE_DIR, "themes", theme, "apply.py") if theme != "default" else os.path.join(BASE_DIR, "themes", "default", "restore.py")
    create_one_click_runner(theme, runner_script, theme_ico)

    # 6. Flush Windows icon cache
    refresh_icon_cache()

    print(f"=== Successfully applied {spec['name']}! ===\n")

if __name__ == "__main__":
    target_theme = sys.argv[1] if len(sys.argv) > 1 else "green"
    apply(target_theme)
