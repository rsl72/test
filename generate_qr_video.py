#!/usr/bin/env python3
"""Generate H.264 video with alternating black/white frames, frame numbers, and QR codes."""

import argparse
import numpy as np
import imageio.v2 as imageio
import qrcode
from PIL import Image, ImageDraw, ImageFont


def make_qr(data: str, size: int, invert: bool = False) -> np.ndarray:
    """Return a QR code image as a NumPy array.

    Args:
        data: Text to encode.
        size: Desired size of the square QR code in pixels.
        invert: If True, invert black/white colors.
    """
    qr = qrcode.QRCode(border=1)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((size, size), Image.NEAREST)
    if invert:
        img = Image.fromarray(255 - np.array(img))
    return np.array(img)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate H.264 video with alternating frames and QR codes.")
    parser.add_argument("output", help="Output video file, e.g. output.mp4")
    parser.add_argument("--width", type=int, default=1280, help="Video width")
    parser.add_argument("--height", type=int, default=720, help="Video height")
    parser.add_argument("--frames", type=int, default=120,
                        help="Number of frames to generate")
    args = parser.parse_args()

    qr_size = min(args.width, args.height) // 4
    writer = imageio.get_writer(args.output, fps=60, codec="libx264", format="mp4")
    font = ImageFont.load_default()

    positions = [
        (0, 0),
        (args.width - qr_size, 0),
        ((args.width - qr_size) // 2, (args.height - qr_size) // 2),
        (0, args.height - qr_size),
        (args.width - qr_size, args.height - qr_size),
    ]

    for frame_num in range(args.frames):
        bg_color = 255 if frame_num % 2 == 0 else 0
        fg_color = 0 if bg_color == 255 else 255
        frame = np.full((args.height, args.width, 3), bg_color, dtype=np.uint8)
        qr_img = make_qr(str(frame_num), qr_size, invert=(bg_color == 0))
        for x, y in positions:
            frame[y:y + qr_size, x:x + qr_size] = qr_img
        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), str(frame_num), fill=(fg_color, fg_color, fg_color),
                  font=font)
        writer.append_data(np.array(img))

    writer.close()


if __name__ == "__main__":
    main()
