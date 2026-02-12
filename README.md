# lockboard

A keyboard/mouse visualizer like NohBoard, made in Python for Linux using **evdev** and **PyGame**, compatible with both **Wayland** and **X11**.

By default, lockboard is set up to match my preferences, but you can customize the key layout in ```lockboard.py``` with a bit of common sense

![Lockboard Showcase](/assets/showcase.png)

## Setup Guide:

1. **Install dependencies** (package names may vary across distros):

   * **Fedora:**

     ```bash
     sudo dnf install python python3-evdev python3-pygame
     ```
   * **Debian/Ubuntu:**

     ```bash
     sudo apt install python3 python3-evdev python3-pygame
     ```
   * **Arch:**

     ```bash
     sudo pacman -S python python-evdev python-pygame
     ```
2. Download and install lockboard's ZIP file.
3. Extract the file and open the folder in a terminal.
4. Run:

   ```bash
   python list-devices.py
   ```

   This will list your keyboard and mouse `/dev/input/event` paths. Make sure it shows your keyboard/mouse name ending with `/input0`.
5. Open `lockboard.py` in a text editor and update the `keyboard` and `mouse` variables to match your `/dev/input/event` paths.
6. Run lockboard:

   ```bash
   python lockboard.py
   ```

---
