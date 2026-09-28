import os
import sys
import subprocess

def get_start_menu_shortcuts():
    return [
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Discord PTB.lnk"),
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Discord Inc\Discord PTB.lnk"),
        os.path.join(os.path.expandvars("%USERPROFILE%"), "Desktop", "Discord PTB.lnk"),
    ]

def patch_shortcuts(icon_path):
    shortcuts = get_start_menu_shortcuts()
    ps_lines = ["$shell = New-Object -ComObject WScript.Shell"]
    safe_ico = icon_path.replace("'", "''")

    for lnk in shortcuts:
        safe_lnk = lnk.replace("'", "''")
        ps_lines.append(
            f"if (Test-Path '{safe_lnk}') {{ "
            f"$sc = $shell.CreateShortcut('{safe_lnk}'); "
            f"$sc.IconLocation = '{safe_ico},0'; "
            f"$sc.Save(); "
            f"Write-Host '  Patched shortcut: {safe_lnk}' }}"
        )

    ps_script = "\n".join(ps_lines)
    result = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script],
                            capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0 and result.stderr.strip():
        print("  Shortcut warning:", result.stderr.strip())

def create_one_click_runner(theme, runner_script, icon_path, desktop=True, shortcuts_dir=True):
    titles = {
        "green": "Fix PTB Green Icon",
        "red": "Fix PTB Red Icon",
        "default": "Restore PTB Default"
    }
    title = titles.get(theme, f"Fix PTB {theme.capitalize()} Icon")
    pythonw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    if not os.path.isfile(pythonw):
        pythonw = sys.executable

    targets = []
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if desktop:
        targets.append(os.path.join(os.path.expandvars("%USERPROFILE%"), "Desktop", f"{title}.lnk"))
    if shortcuts_dir:
        targets.append(os.path.join(base_dir, "shortcuts", f"{title}.lnk"))

    ps_lines = ["$shell = New-Object -ComObject WScript.Shell"]
    safe_py = pythonw.replace("'", "''")
    safe_script = runner_script.replace("'", "''")
    safe_workdir = base_dir.replace("'", "''")
    safe_ico = icon_path.replace("'", "''")

    for t in targets:
        os.makedirs(os.path.dirname(t), exist_ok=True)
        safe_t = t.replace("'", "''")
        ps_lines.append(
            f"$sc = $shell.CreateShortcut('{safe_t}'); "
            f"$sc.TargetPath = '{safe_py}'; "
            f"$sc.Arguments = '\"' + '{safe_script}' + '\"'; "
            f"$sc.WorkingDirectory = '{safe_workdir}'; "
            f"$sc.IconLocation = '{safe_ico},0'; "
            f"$sc.Description = 'Applies {theme.capitalize()} Theme to Discord PTB'; "
            f"$sc.Save(); "
            f"Write-Host '  Configured runner: {safe_t}'"
        )

    ps_script = "\n".join(ps_lines)
    result = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script],
                            capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
