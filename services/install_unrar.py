# services/install_ssh.py
from common.utils import run_cmd
import os

def install_unrar():
    run_cmd(["sudo", "apt", "install", "unrar", "-y"])

