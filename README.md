# Kiran's Star-Style ASCII Birthday Surprise ✨

A Python application that transforms photos into animated, star-filled (`*`) ASCII art portraits with a DJ remix-style reveal effect and displays a grand, custom star-bordered birthday banner.

---

## Features

- **Photo Import System**:
  - Automatically detects photos (such as `Kiran Ph.jpeg`) placed in the folder for instant 1-click selection.
  - Graphical File Picker (`tkinter.filedialog`) to browse and select any image file with a single click.
  - Manual file path entry support as a robust fallback.
  - Supports all major formats: JPG, JPEG, PNG, BMP, WEBP, TIFF.

- **DJ Remix Inward Onion-Peel Animation**:
  - Automatically binarizes portraits using Otsu's thresholding and dynamic contrast enhancement.
  - Efficient multi-source breadth-first search ($O(W \times H)$) detects the person's outer contour.
  - Renders the outer contour first using `*` characters and progressively fills inward layer-by-layer.
  - Visual DJ equalizer header and optional rhythmic synth beat sound effects (on Windows).
  - Terminal-friendly rendering using ANSI escape cursor resets for smooth, flicker-free playback.
  - Non-animated mode available for simple terminals or logging.

- **Grand ASCII Birthday Banner**:
  - Large decorative 5x5 block letter font rendering: `HAPPY BIRTHDAY KIRAN!`.
  - Star-shaped border ornaments and frame.
  - Dynamically wraps words and auto-scales to ensure text is never clipped or distorted regardless of console width.

- **Beginner-Friendly & Cross-Platform**:
  - Works on Windows, macOS, and Linux.
  - Safe 100% standard ASCII output with automatic terminal encoding detection.
  - Ready to run immediately: just press **Enter** to accept all default settings!

---

## 1. How to Install Python

### Windows
1. Download Python 3.10 or later from the official website: [python.org/downloads](https://www.python.org/downloads/).
2. During installation, make sure to check the box: **"Add Python to PATH"**.
3. Verify installation in PowerShell or Command Prompt:
   ```powershell
   python --version
   ```

### macOS
1. Install using Homebrew:
   ```bash
   brew install python
   ```
2. Verify installation in Terminal:
   ```bash
   python3 --version
   ```

### Linux (Ubuntu / Debian)
1. Install using `apt`:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-tk
   ```
2. Verify installation:
   ```bash
   python3 --version
   ```

---

## 2. How to Install Dependencies

The only external dependency is **Pillow** (PIL) for image decoding and processing. Standard Python libraries are used for everything else.

From the project directory:

### Windows (PowerShell / Command Prompt):
```powershell
pip install -r requirements.txt
```
*(Or directly: `pip install Pillow`)*

### macOS / Linux:
```bash
pip3 install -r requirements.txt
```

---

## 3. How to Run the Application

### Quick Start (Interactive Wizard)
From the project folder, simply execute:

#### Windows:
```powershell
python main.py
```

#### macOS / Linux:
```bash
python3 main.py
```

When prompted:
1. **Photo**: Press `Enter` to use the automatically detected photo (e.g. `Kiran Ph.jpeg`), or select `2` to open the graphical file picker.
2. **Name**: Press `Enter` to keep the default name (`Kiran`), or enter a custom name.
3. **Width**: Press `Enter` to keep the default width (`80`), or enter a preferred width (e.g. `100`).
4. **Brightness Invert**: Press `Enter` for the recommended setting.
5. **Animation**: Press `Enter` to enjoy the inward star reveal animation.
6. **Speed**: Choose tempo `1` (Normal), `2` (Fast), `3` (DJ Turbo), or `4` (Relaxed).
7. Sit back and watch the animated DJ star reveal drop into the grand birthday banner!

---

## 4. How to Configure Options via Command-Line Flags

For automated runs, custom scripts, or fast execution without prompts, you can pass command-line arguments:

```bash
python main.py --image "Kiran Ph.jpeg" --name "Kiran" --width 80 --speed 0.03
```

### Available Flags:

| Flag | Description | Default | Example |
| :--- | :--- | :--- | :--- |
| `--image`, `-i` | Path to photo image file | Prompts user | `--image "Kiran Ph.jpeg"` |
| `--name`, `-n` | Birthday person's name | `Kiran` | `--name "Kiran"` |
| `--width`, `-w` | Console width in columns | `80` | `--width 90` |
| `--no-anim` | Disable animation; render directly | False | `--no-anim` |
| `--speed`, `-s` | Animation frame delay (seconds) | `0.04` (40ms) | `--speed 0.02` |
| `--invert` | Force invert brightness | Auto-detected | `--invert` |
| `--no-invert` | Force normal brightness | Auto-detected | `--no-invert` |
| `--sound` | Enable DJ audio sound effects (Windows) | Disabled | `--sound` |
| `--no-sound` | Disable sound effects | True | `--no-sound` |
| `--test` | Run automated self-test | False | `--test` |

---

## 5. Troubleshooting Common Issues

### 1. `ModuleNotFoundError: No module named 'PIL'`
- **Cause**: Pillow is not yet installed in your active Python environment.
- **Fix**: Run `pip install Pillow` or `python -m pip install -r requirements.txt`.

### 2. File Picker Doesn't Appear
- **Cause**: Tkinter window might be hidden behind other windows, or running in a headless SSH session.
- **Fix**: Check your taskbar for the open file dialog, or choose the manual path option by typing the file name directly.

### 3. Portrait Appears Too Wide or Stretched
- **Cause**: Non-standard terminal monospace font aspect ratio.
- **Fix**: Increase terminal window size or pass a smaller width, e.g. `--width 70`.

### 4. Background is Filled with Stars Instead of Person
- **Cause**: High-brightness contrast inversion mismatch.
- **Fix**: When prompted, toggle the **Invert Brightness** option (`Y` or `n`), or run with `--invert` / `--no-invert`.

### 5. Screen Flickers During Animation
- **Cause**: Legacy terminal without virtual terminal ANSI support.
- **Fix**: Use modern **Windows Terminal**, **PowerShell 7**, or pass `--no-anim` for direct rendering.

---

## Project Structure

```
birthday_ascii/
│   main.py             # Complete application code
│   requirements.txt    # Pillow dependency specification
│   README.md           # Instructions, configuration, and troubleshooting
│   .gitignore          # Git exclusion rules for Python caches and venvs
```

Enjoy the birthday celebration! 🎉
"# KiranBirthday_Spec" 
