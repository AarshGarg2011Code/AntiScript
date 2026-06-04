# AntiScript v1.0.0
# Made by Aarsh Garg in 2026.
# Module 'cmdlets'
import subprocess
import tempfile
import os
import sys

IS_WINDOWS = sys.platform.startswith("win")

def cmdlets_run(command, ishidden=True):
    cmd = str(command)

    try:
        if ishidden and IS_WINDOWS:
            return subprocess.run(
                cmd,
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            return subprocess.run(
                cmd,
                shell=True
            )
    except Exception as e:
        print(f"[cmdlets_run error] {e}")


def cmdlets_run_bat(snippet: str, ishidden: bool = False, capture_output: bool = False, echo: bool = False):

    script = snippet if echo else "@echo off\n" + snippet

    with tempfile.NamedTemporaryFile(delete=False, suffix=".bat", mode="w", encoding="utf-8") as f:
        f.write(script)
        bat_path = f.name

    try:
        kwargs = {
            "args": ["cmd", "/c", bat_path],
            "capture_output": capture_output,
            "text": True
        }

        if ishidden and IS_WINDOWS:
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

        result = subprocess.run(**kwargs)

        return result if capture_output else None

    finally:
        os.remove(bat_path)


def cmdlets_cmd():
    subprocess.run("cmd", shell=True)


def cmdlets_powershell():
    subprocess.run("powershell", shell=True)