"""Kiran's Star-Style ASCII Birthday Surprise.

A complete Python application that transforms a user's photo into an animated,
star-filled ASCII portrait with a DJ remix-style reveal effect and presents a
festive, custom star-bordered birthday banner.

Requirements:
    - Python 3.10+
    - Pillow (PIL)
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import threading
import time
from typing import Dict, List, Optional, Tuple

# Ensure safe output stream encoding across Windows / macOS / Linux
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    from PIL import Image, ImageEnhance, ImageOps
except ImportError:
    print(
        "\n[ERROR] The 'Pillow' library is required to run this application.\n"
        "Please install it using:\n"
        "    pip install Pillow\n"
        "or\n"
        "    pip install -r requirements.txt\n"
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# ASCII Font Definitions (5x5 Grid for each character)
# ---------------------------------------------------------------------------
BANNER_GLYPHS: Dict[str, List[str]] = {
    "A": [" *** ", "*   *", "*****", "*   *", "*   *"],
    "B": ["**** ", "*   *", "**** ", "*   *", "**** "],
    "C": [" ****", "*    ", "*    ", "*    ", " ****"],
    "D": ["**** ", "*   *", "*   *", "*   *", "**** "],
    "E": ["*****", "*    ", "**** ", "*    ", "*****"],
    "F": ["*****", "*    ", "**** ", "*    ", "*    "],
    "G": [" ****", "*    ", "* ***", "*   *", " ****"],
    "H": ["*   *", "*   *", "*****", "*   *", "*   *"],
    "I": ["*****", "  *  ", "  *  ", "  *  ", "*****"],
    "J": ["  ***", "   * ", "   * ", "*  * ", " **  "],
    "K": ["*   *", "*  * ", "***  ", "*  * ", "*   *"],
    "L": ["*    ", "*    ", "*    ", "*    ", "*****"],
    "M": ["*   *", "** **", "* * *", "*   *", "*   *"],
    "N": ["*   *", "**  *", "* * *", "*  **", "*   *"],
    "O": [" *** ", "*   *", "*   *", "*   *", " *** "],
    "P": ["**** ", "*   *", "**** ", "*    ", "*    "],
    "Q": [" *** ", "*   *", "* * *", "*  **", " ****"],
    "R": ["**** ", "*   *", "**** ", "*  * ", "*   *"],
    "S": [" ****", "*    ", " *** ", "    *", "**** "],
    "T": ["*****", "  *  ", "  *  ", "  *  ", "  *  "],
    "U": ["*   *", "*   *", "*   *", "*   *", " *** "],
    "V": ["*   *", "*   *", "*   *", " * * ", "  *  "],
    "W": ["*   *", "*   *", "* * *", "** **", "*   *"],
    "X": ["*   *", " * * ", "  *  ", " * * ", "*   *"],
    "Y": ["*   *", " * * ", "  *  ", "  *  ", "  *  "],
    "Z": ["*****", "   * ", "  *  ", " *   ", "*****"],
    "0": [" *** ", "*  **", "* * *", "**  *", " *** "],
    "1": ["  *  ", " **  ", "  *  ", "  *  ", " *** "],
    "2": [" *** ", "*   *", "  ** ", " *   ", "*****"],
    "3": ["**** ", "    *", " *** ", "    *", "**** "],
    "4": ["*  * ", "*  * ", "*****", "   * ", "   * "],
    "5": ["*****", "*    ", "**** ", "    *", "**** "],
    "6": [" *** ", "*    ", "**** ", "*   *", " *** "],
    "7": ["*****", "    *", "   * ", "  *  ", " *   "],
    "8": [" *** ", "*   *", " *** ", "*   *", " *** "],
    "9": [" *** ", "*   *", " ****", "    *", " *** "],
    " ": ["     ", "     ", "     ", "     ", "     "],
    "!": ["  *  ", "  *  ", "  *  ", "     ", "  *  "],
    "?": ["***  ", "   * ", "  *  ", "     ", "  *  "],
    ".": ["     ", "     ", "     ", "     ", "  *  "],
    "-": ["     ", "     ", " *** ", "     ", "     "],
    "+": ["     ", "  *  ", " *** ", "  *  ", "     "],
    ":": ["     ", "  *  ", "     ", "  *  ", "     "],
    "*": [" * * ", "  *  ", "*****", "  *  ", " * * "],
}

FALLBACK_GLYPH = ["*****", "*   *", "*   *", "*   *", "*****"]


# ---------------------------------------------------------------------------
# Terminal Configuration and ANSI Helper
# ---------------------------------------------------------------------------
def setup_terminal() -> bool:
    """Enable ANSI virtual terminal processing on Windows if applicable.

    Returns True if ANSI sequences are supported, False otherwise.
    """
    if os.name == "nt":
        # Windows command prompt / PowerShell ANSI support
        try:
            os.system("")
            return True
        except Exception:
            return False
    return sys.stdout.isatty()


def clear_screen(use_ansi: bool = True) -> None:
    """Clear terminal screen or reposition cursor to home."""
    if use_ansi:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
    else:
        os.system("cls" if os.name == "nt" else "clear")


def cursor_home(use_ansi: bool = True) -> None:
    """Move cursor to top-left without clearing to eliminate screen flicker."""
    if use_ansi:
        sys.stdout.write("\033[H")
        sys.stdout.flush()
    else:
        clear_screen(False)


# ---------------------------------------------------------------------------
# Audio / DJ Sound Beat (Graceful Windows & Cross-Platform Support)
# ---------------------------------------------------------------------------
def play_dj_sound(frequency: int, duration_ms: int) -> None:
    """Play a short synth sound on Windows in a background thread without lag."""
    if os.name == "nt":
        try:
            import winsound

            threading.Thread(
                target=winsound.Beep,
                args=(max(37, min(32767, frequency)), duration_ms),
                daemon=True,
            ).start()
        except Exception:
            pass


def play_bass_drop() -> None:
    """Play a celebratory DJ bass drop sequence."""
    if os.name == "nt":
        def _drop_sequence():
            try:
                import winsound

                for freq in [600, 750, 900, 1100, 1400]:
                    winsound.Beep(freq, 40)
                    time.sleep(0.01)
                winsound.Beep(523, 250)
            except Exception:
                pass

        threading.Thread(target=_drop_sequence, daemon=True).start()


# ---------------------------------------------------------------------------
# Image Detection and File Selection
# ---------------------------------------------------------------------------
SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
    ".tiff",
    ".tif",
}


def find_nearby_images() -> List[Path]:
    """Search current directory, parent directory, and script directory for images."""
    found: List[Path] = []
    seen = set()

    search_dirs = [
        Path.cwd(),
        Path(__file__).resolve().parent,
        Path.cwd().parent,
        Path(__file__).resolve().parent.parent,
    ]

    for d in search_dirs:
        try:
            if not d.exists() or not d.is_dir():
                continue
            for item in sorted(d.iterdir()):
                if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS:
                    resolved = item.resolve()
                    if resolved not in seen:
                        seen.add(resolved)
                        found.append(item)
        except Exception:
            continue

    return found


def pick_image_gui() -> Optional[str]:
    """Launch a graphical file picker using Tkinter filedialog."""
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        selected = filedialog.askopenfilename(
            title="Select Birthday Photo for Star-Style ASCII Art",
            filetypes=[
                (
                    "Image files",
                    "*.jpg;*.jpeg;*.png;*.bmp;*.webp;*.tiff;*.tif",
                ),
                ("All files", "*.*"),
            ],
        )
        root.destroy()
        if selected and os.path.isfile(selected):
            return selected
        return None
    except Exception:
        return None


def select_photo_interactive() -> str:
    """Prompt user to select a photo with automatic detection, GUI picker, and manual path."""
    nearby_images = find_nearby_images()

    print("\n" + "=" * 70)
    print("               PHOTO SELECTION".center(70))
    print("=" * 70)

    options_map: Dict[str, str] = {}
    idx = 1

    if nearby_images:
        print("\nDiscovered photos in your folder:")
        for img_path in nearby_images[:4]:
            print(f"  [{idx}] Use detected photo: {img_path.name}")
            options_map[str(idx)] = str(img_path.resolve())
            idx += 1

    gui_option = str(idx)
    print(f"  [{gui_option}] Open Graphical File Picker (Browse dialog)")
    idx += 1

    manual_option = str(idx)
    print(f"  [{manual_option}] Enter image path manually")

    default_choice = "1" if nearby_images else gui_option

    while True:
        prompt_text = (
            f"\nSelect an option [1-{manual_option}, Default: {default_choice}]: "
        )
        choice = input(prompt_text).strip()
        if not choice:
            choice = default_choice

        if choice in options_map:
            chosen_path = options_map[choice]
            if os.path.isfile(chosen_path):
                print(f"[OK] Selected: {Path(chosen_path).name}")
                return chosen_path
            print(f"[ERROR] File not found: {chosen_path}")

        elif choice == gui_option:
            print("[INFO] Opening file dialog... Please check for the file picker window.")
            chosen_path = pick_image_gui()
            if chosen_path:
                print(f"[OK] Selected: {chosen_path}")
                return chosen_path
            print("[NOTICE] No file was selected from the dialog. You can choose another option.")

        elif choice == manual_option:
            while True:
                path_input = input("\nEnter full path to image file (or 'back'): ").strip().strip('"\'')
                if path_input.lower() == "back":
                    break
                if not path_input:
                    continue
                if os.path.isfile(path_input):
                    print(f"[OK] Verified image path: {path_input}")
                    return path_input
                print(f"[ERROR] Cannot find or open file: '{path_input}'. Please check the path.")
        else:
            # Check if user typed a direct path directly into the main prompt
            cleaned = choice.strip('"\'')
            if os.path.isfile(cleaned):
                return cleaned
            print(f"[ERROR] Invalid option '{choice}'. Please enter a valid number.")


# ---------------------------------------------------------------------------
# Image Processing & Foreground Mask Generation
# ---------------------------------------------------------------------------
def compute_otsu_threshold(image: Image.Image) -> int:
    """Compute optimal binarization threshold using Otsu's method."""
    histogram = image.histogram()
    total_pixels = image.width * image.height
    if total_pixels == 0:
        return 128

    sum_all = sum(i * histogram[i] for i in range(256))
    weight_bg = 0
    sum_bg = 0
    max_variance = -1.0
    threshold = 128

    for t in range(256):
        weight_bg += histogram[t]
        if weight_bg == 0:
            continue
        weight_fg = total_pixels - weight_bg
        if weight_fg == 0:
            break

        sum_bg += t * histogram[t]
        mean_bg = sum_bg / weight_bg
        mean_fg = (sum_all - sum_bg) / weight_fg

        variance_between = weight_bg * weight_fg * ((mean_bg - mean_fg) ** 2)
        if variance_between > max_variance:
            max_variance = variance_between
            threshold = t

    return threshold


def detect_bright_background(image: Image.Image) -> bool:
    """Determine whether photo has a light background based on corner pixels.

    Uses corners (not full border) to avoid sampling the subject's body edges.
    Returns True if background is bright (invert needed for dark-subject photos).
    """
    w, h = image.size
    # Sample only the 4 corners (5% of each dimension) — most reliable background indicator
    corner_size_x = max(1, w // 20)
    corner_size_y = max(1, h // 20)
    corner_pixels = []
    for cy in range(corner_size_y):
        for cx in range(corner_size_x):
            corner_pixels.append(image.getpixel((cx, cy)))                    # top-left
            corner_pixels.append(image.getpixel((w - 1 - cx, cy)))           # top-right
            corner_pixels.append(image.getpixel((cx, h - 1 - cy)))           # bottom-left
            corner_pixels.append(image.getpixel((w - 1 - cx, h - 1 - cy)))  # bottom-right

    avg_corner = sum(corner_pixels) / max(len(corner_pixels), 1)
    return avg_corner >= 140


# ---------------------------------------------------------------------------
# ASCII Density Ramp (dark → light maps to dense → sparse characters)
# ---------------------------------------------------------------------------
# ASCII_RAMP: ordered darkest (densest) to lightest (emptiest).
# This classic ramp gives excellent face/body definition at terminal widths.
ASCII_RAMP = "@#S%?*+;:,. "
RAMP_LEN = len(ASCII_RAMP)


def load_and_preprocess_image(
    image_path: str,
    target_width: int = 100,
    char_aspect_ratio: float = 0.45,
) -> Tuple[Image.Image, int, int]:
    """Load image, enhance contrast sharply, and scale to console aspect ratio."""
    try:
        with Image.open(image_path) as raw_img:
            img = raw_img.convert("L")
    except Exception as exc:
        raise ValueError(f"Could not open image file '{image_path}': {exc}") from exc

    # Strong autocontrast + gamma + sharpness to bring out facial features
    img = ImageOps.autocontrast(img, cutoff=3)
    # Gamma correction: darken midtones to increase face/shadow contrast
    gamma_table = [int((i / 255) ** 0.7 * 255) for i in range(256)]
    img = img.point(gamma_table)
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = ImageEnhance.Sharpness(img).enhance(2.5)

    orig_w, orig_h = img.size
    if orig_w == 0 or orig_h == 0:
        raise ValueError("Image dimensions cannot be zero.")

    target_width = max(40, target_width)
    # char_aspect_ratio < 0.5 compensates for monospace chars being taller than wide
    target_height = max(20, int((orig_h / orig_w) * target_width * char_aspect_ratio))

    resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    return resized, target_width, target_height


def image_to_ascii_grid(
    image: Image.Image,
    invert: bool,
    width: int,
    height: int,
) -> List[str]:
    """Convert every pixel to an ASCII character based on brightness density.

    Each pixel brightness (0-255) maps to a character in ASCII_RAMP so that
    all facial features — eyes, nose, lips, hair, neck, hands — are preserved
    as distinct characters rather than collapsed to a binary mask.
    """
    rows: List[str] = []
    for y in range(height):
        row_chars = []
        for x in range(width):
            brightness = image.getpixel((x, y))  # 0 (black) – 255 (white)
            if invert:
                brightness = 255 - brightness
            # Map brightness to ramp index: 0 → index 0 (densest), 255 → last (space)
            idx = int(brightness / 255 * (RAMP_LEN - 1))
            row_chars.append(ASCII_RAMP[idx])
        rows.append("".join(row_chars))
    return rows


# ---------------------------------------------------------------------------
# Birthday Banner Generation
# ---------------------------------------------------------------------------
def render_big_word(word: str) -> List[str]:
    """Render a single uppercase word using 5x5 ASCII block letter glyphs."""
    word = word.upper()
    lines = ["", "", "", "", ""]
    for char in word:
        glyph = BANNER_GLYPHS.get(char, FALLBACK_GLYPH)
        for i in range(5):
            lines[i] += glyph[i] + " "
    return [l.rstrip() for l in lines]


def generate_birthday_banner(
    recipient_name: str = "KIRAN",
    target_width: int = 80,
) -> str:
    """Generate a decorative star-shaped border ASCII banner with HAPPY BIRTHDAY [NAME]!.

    Dynamically wraps words if the console width is narrow so it never gets cut off.
    """
    width = max(40, target_width)
    inner_width = width - 4  # accounted for 2 stars on each side

    # Determine word blocks
    clean_name = recipient_name.strip().upper()
    if not clean_name.endswith("!"):
        clean_name += "!"

    hb_lines = render_big_word("HAPPY BIRTHDAY")
    name_lines = render_big_word(clean_name)

    banner_blocks: List[List[str]] = []

    # Check if HAPPY BIRTHDAY fits on one line
    if len(hb_lines[0]) <= inner_width:
        banner_blocks.append(hb_lines)
    else:
        # Wrap into HAPPY and BIRTHDAY separately
        banner_blocks.append(render_big_word("HAPPY"))
        banner_blocks.append(render_big_word("BIRTHDAY"))

    # Check if recipient name fits
    if len(name_lines[0]) <= inner_width:
        banner_blocks.append(name_lines)
    else:
        # Split name words or compact fallback
        name_words = clean_name.split()
        if len(name_words) > 1 and all(len(render_big_word(w)[0]) <= inner_width for w in name_words):
            for w in name_words:
                banner_blocks.append(render_big_word(w))
        else:
            compact_line = f"*** {clean_name} ***"
            banner_blocks.append([compact_line.center(inner_width)])

    # Construct decorative star frame
    output: List[str] = []

    star_crest_small = "* * *"
    star_crest_large = "* * * * *"
    gap = max(2, width - 26)

    crest_1 = f"    {star_crest_small}{' ' * gap}{star_crest_small}    ".center(width)
    crest_2 = f"  {star_crest_large}{' ' * max(2, gap - 4)}{star_crest_large}  ".center(width)

    output.append("")
    output.append(crest_1)
    output.append(crest_2)
    output.append(crest_1)

    # Top border with solid stars
    output.append("*" * width)
    output.append("**" + " " * (width - 4) + "**")

    # Content blocks centered inside star borders
    for b_idx, block in enumerate(banner_blocks):
        for line in block:
            centered = line.center(width - 4)
            output.append(f"**{centered}**")
        if b_idx < len(banner_blocks) - 1:
            output.append("**" + " " * (width - 4) + "**")

    # Bottom border
    output.append("**" + " " * (width - 4) + "**")
    output.append("*" * width)

    # Inverted star footer
    output.append(crest_1)
    output.append(crest_2)
    output.append(crest_1)
    output.append("")

    return "\n".join(output)


# ---------------------------------------------------------------------------
# Animation & Presentation Controller
# ---------------------------------------------------------------------------
DJ_EQUALIZER_FRAMES = [
    "[|||||     * DJ REMIX: STAR OUTLINE DROP *     |||||]",
    "[||||||||  * DJ REMIX: INWARD STAR REVEAL *  ||||||||]",
    "[||||||||||* DJ REMIX: FEEL THE BEAT PULSE*||||||||||]",
    "[||||||||  * DJ REMIX: SURPRISE INCOMING! *  ||||||||]",
]


def render_ascii_portrait(
    ascii_rows: List[str],
    reveal_up_to_row: int,
    height: int,
) -> str:
    """Render the ASCII portrait revealing rows top-to-bottom for the DJ sweep animation."""
    visible = ascii_rows[:reveal_up_to_row]
    # Pad remaining rows with blank lines so the frame height stays stable
    blank = " " * (len(ascii_rows[0]) if ascii_rows else 0)
    padded = visible + [blank] * (height - len(visible))
    return "\n".join(padded)


def run_dj_birthday_surprise(
    image_path: str,
    recipient_name: str = "Kiran",
    console_width: int = 100,
    animate: bool = True,
    frame_delay: float = 0.04,
    invert: Optional[bool] = None,
    threshold: Optional[int] = None,
    sound_enabled: bool = True,
) -> None:
    """Execute the complete Star-Style ASCII Birthday Surprise."""
    use_ansi = setup_terminal()

    # Step 1: Preprocess Image
    print("\n[1/3] Loading and analyzing photo...")
    processed_img, width, height = load_and_preprocess_image(
        image_path,
        target_width=console_width,
    )

    # Auto-detect inversion: bright background → invert so face is dense chars
    is_light_bg = detect_bright_background(processed_img)
    if invert is None:
        invert = is_light_bg

    # Step 2: Build full-detail ASCII grid (every pixel → a character)
    print("[2/3] Mapping photo pixels to ASCII density characters...")
    ascii_rows = image_to_ascii_grid(processed_img, invert=invert, width=width, height=height)

    time.sleep(0.3)

    # Step 3: Animated top-to-bottom DJ sweep reveal
    if animate:
        clear_screen(use_ansi)
        for row_count in range(1, height + 1):
            eq_text = DJ_EQUALIZER_FRAMES[(row_count - 1) % len(DJ_EQUALIZER_FRAMES)]
            header = f"\n{eq_text.center(width)}\n"
            status = f"--- [ REVEAL: ROW {row_count:03d}/{height:03d} ] ---".center(width)

            portrait_text = render_ascii_portrait(ascii_rows, row_count, height)

            cursor_home(use_ansi)
            sys.stdout.write(header + status + "\n" + portrait_text + "\n")
            sys.stdout.flush()

            if sound_enabled:
                beat_freq = 400 + int((row_count / height) * 600)
                play_dj_sound(beat_freq, max(15, int(frame_delay * 600)))

            time.sleep(frame_delay)

    # Step 4: Final Complete Portrait Display
    clear_screen(use_ansi)
    final_header = f"=== * PHOTO-REALISTIC ASCII PORTRAIT OF {recipient_name.upper()} * ===".center(width)
    final_portrait = "\n".join(ascii_rows)

    print("\n" + final_header)
    print(final_portrait)

    # Drop the DJ celebratory bass beat!
    if sound_enabled and animate:
        play_bass_drop()
        time.sleep(0.2)

    # Step 5: Grand Birthday Banner Finale
    banner = generate_birthday_banner(recipient_name=recipient_name, target_width=width)
    print(banner)

    # Completion greetings
    print(f"Wishing {recipient_name} a fabulous birthday filled with joy and stars! * *\n")


# ---------------------------------------------------------------------------
# Interactive Menu Wizard
# ---------------------------------------------------------------------------
def run_interactive_wizard() -> None:
    """Run beginner-friendly interactive configuration wizard."""
    setup_terminal()
    clear_screen(False)

    print("*" * 72)
    print("*" + " " * 70 + "*")
    print("*" + "*  KIRAN'S STAR-STYLE ASCII BIRTHDAY SURPRISE  *".center(70) + "*")
    print("*" + "Animated DJ Remix Star Portrait & Grand Birthday Banner".center(70) + "*")
    print("*" + " " * 70 + "*")
    print("*" * 72)

    # 1. Image Selection
    photo_path = select_photo_interactive()

    # 2. Recipient Name
    print("\n" + "-" * 70)
    name_input = input("Enter Birthday Person's Name [Default: Kiran]: ").strip()
    recipient_name = name_input if name_input else "Kiran"

    # 3. Console Width
    while True:
        width_input = input("Enter Console Display Width (columns) [Default: 100]: ").strip()
        if not width_input:
            console_width = 100
            break
        try:
            val = int(width_input)
            if 30 <= val <= 250:
                console_width = val
                break
            print("[NOTICE] Please choose a width between 30 and 250.")
        except ValueError:
            print("[ERROR] Please enter a valid number.")

    # 4. Invert Brightness Setting
    print("\n" + "-" * 70)
    print("Brightness Mode:")
    print("  Photos with bright/white backgrounds look best INVERTED (subject rendered in *).")
    print("  Photos with dark backgrounds look best in NORMAL mode.")
    invert_choice = input("Invert brightness for bright background photo? (Y/n) [Default: Y]: ").strip().lower()
    invert = invert_choice != "n"

    # 5. Animation Option
    anim_choice = input("\nEnable animated inward star reveal? (Y/n) [Default: Y]: ").strip().lower()
    animate = anim_choice != "n"

    # 6. Animation Speed
    frame_delay = 0.04
    if animate:
        print("\nChoose DJ Animation Speed:")
        print("  [1] Normal Tempo   (40ms / frame) - Recommended")
        print("  [2] Fast Beat      (20ms / frame)")
        print("  [3] DJ Turbo Beat  (10ms / frame)")
        print("  [4] Slow & Smooth  (80ms / frame)")
        speed_choice = input("Select speed [1-4, Default: 1]: ").strip()
        speed_map = {"1": 0.04, "2": 0.02, "3": 0.01, "4": 0.08}
        frame_delay = speed_map.get(speed_choice, 0.04)

    # 7. Sound Effect (Windows only)
    sound_enabled = False
    if os.name == "nt" and animate:
        sound_choice = input("\nEnable DJ synth audio beats? (Y/n) [Default: Y]: ").strip().lower()
        sound_enabled = sound_choice != "n"

    print("\n" + "=" * 70)
    print("Starting Star Birthday Surprise in 3... 2... 1...".center(70))
    print("=" * 70)
    time.sleep(1.0)

    run_dj_birthday_surprise(
        image_path=photo_path,
        recipient_name=recipient_name,
        console_width=console_width,
        animate=animate,
        frame_delay=frame_delay,
        invert=invert,
        sound_enabled=sound_enabled,
    )


# ---------------------------------------------------------------------------
# CLI Argument Parser (For Automation, Scripting & Direct Execution)
# ---------------------------------------------------------------------------
def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Kiran's Star-Style ASCII Birthday Surprise - Animated ASCII portrait and banner generator."
    )
    parser.add_argument(
        "--image", "-i",
        type=str,
        default=None,
        help="Path to photo image file (JPG, PNG, BMP, etc.).",
    )
    parser.add_argument(
        "--name", "-n",
        type=str,
        default=None,
        help="Recipient's name (default: Kiran).",
    )
    parser.add_argument(
        "--width", "-w",
        type=int,
        default=None,
        help="Console display width in characters (default: 80).",
    )
    parser.add_argument(
        "--no-anim",
        action="store_true",
        help="Disable animation and render directly.",
    )
    parser.add_argument(
        "--speed", "-s",
        type=float,
        default=None,
        help="Animation delay in seconds (e.g., 0.04 for 40ms).",
    )
    parser.add_argument(
        "--invert",
        action="store_true",
        help="Force invert brightness.",
    )
    parser.add_argument(
        "--no-invert",
        action="store_true",
        help="Force disable invert brightness.",
    )
    parser.add_argument(
        "--sound",
        action="store_true",
        help="Enable DJ sound beats.",
    )
    parser.add_argument(
        "--no-sound",
        action="store_true",
        help="Disable sound beats.",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run self-test with an internally generated test portrait.",
    )
    return parser.parse_args()


def run_self_test() -> None:
    """Run self-test with a generated gradient image to verify ASCII density mapping."""
    print("\n--- Running ASCII Birthday Surprise Self-Test ---")
    test_img = Image.new("L", (100, 80), color=255)
    # Gradient: dark circle (face) on white background
    for y in range(80):
        for x in range(100):
            dist = ((x - 50) ** 2 + (y - 40) ** 2) ** 0.5
            if dist < 30:
                # Vary brightness inside circle to simulate facial shading
                brightness = int(30 + dist * 4)
                test_img.putpixel((x, y), min(255, brightness))

    test_path = "test_sample_portrait.png"
    test_img.save(test_path)
    try:
        run_dj_birthday_surprise(
            image_path=test_path,
            recipient_name="Kiran",
            console_width=60,
            animate=False,
            sound_enabled=False,
        )
        print("[SUCCESS] Self-test completed successfully!")
    finally:
        if os.path.exists(test_path):
            os.remove(test_path)


def main() -> None:
    """Application entry point."""
    args = parse_arguments()

    if args.test:
        run_self_test()
        return

    # If image or parameters were passed via CLI flags, run directly
    if args.image:
        if not os.path.isfile(args.image):
            print(f"[ERROR] Specified image file not found: '{args.image}'")
            sys.exit(1)

        name = args.name if args.name else "Kiran"
        width = args.width if args.width else 100
        animate = not args.no_anim
        speed = args.speed if args.speed is not None else 0.04
        invert_flag = True if args.invert else (False if args.no_invert else None)
        sound_flag = False if args.no_sound else (True if args.sound else False)

        run_dj_birthday_surprise(
            image_path=args.image,
            recipient_name=name,
            console_width=width,
            animate=animate,
            frame_delay=speed,
            invert=invert_flag,
            sound_enabled=sound_flag,
        )
        return

    # Otherwise run the interactive wizard
    try:
        run_interactive_wizard()
    except KeyboardInterrupt:
        print("\n\n[NOTICE] Birthday surprise exited. Have a wonderful celebration! * *\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
