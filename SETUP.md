# Setup Guide

This project is a `pyglet` desktop game and works best with a local virtual environment.

## 1) Prerequisites

- Python 3.10+
- `pip`
- OpenGL runtime (Linux only)

### Linux (Ubuntu/Debian)

Install system packages:

```bash
sudo apt-get update
sudo apt-get install -y python3-venv libglu1-mesa
```

## 2) Create and activate a virtual environment

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

## 3) Install Python dependencies

```bash
pip install -r requirements.txt
```

## 4) Run the game client

```bash
python main.py
```

## 5) (Optional) Run the server

In a second terminal from the project root:

```bash
python server_framework/server.py
```

## VS Code

- Use the launch profile `Python: Main` in `.vscode/launch.json`.
- If needed, select `.venv/bin/python` as interpreter.

## Notes

- If you see `Library "GLU" not found`, install `libglu1-mesa` (Linux).
- If your distro blocks global `pip` installs (`externally-managed-environment`), always install inside `.venv`.