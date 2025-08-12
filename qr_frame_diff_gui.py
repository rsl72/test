#!/usr/bin/env python3
"""GUI tool to analyze frame differences between QR codes in a video."""

import argparse
import csv
import numpy as np
import cv2


def select_rois(frame):

    """Display a GUI to select two regions of interest containing QR codes.

    After selecting two areas, press the *Enter* key to begin analysis.
    """

    import tkinter as tk
    from PIL import Image, ImageTk

    rois = []
    root = tk.Tk()
    root.title("Select two QR code areas")

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    photo = ImageTk.PhotoImage(img)
    canvas = tk.Canvas(root, width=img.width, height=img.height)
    canvas.pack()
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)

    current = {"start": None, "rect": None}

    def on_press(event):
        if len(rois) >= 2:
            return
        current["start"] = (event.x, event.y)
        current["rect"] = canvas.create_rectangle(
            event.x, event.y, event.x, event.y, outline="red")

    def on_drag(event):
        if current["rect"]:
            canvas.coords(current["rect"], current["start"][0], current["start"][1],
                          event.x, event.y)

    def on_release(event):
        if current["rect"]:
            x0, y0 = current["start"]
            rois.append((min(x0, event.x), min(y0, event.y),
                         max(x0, event.x), max(y0, event.y)))
            current["rect"] = None

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)

    def on_ok():
        if len(rois) == 2:
            root.destroy()

    tk.Button(root, text="OK", command=on_ok).pack()

    root.bind("<Return>", lambda _event: on_ok())

    root.mainloop()
    return rois


def analyze(video_path: str, fps: float, roi1, roi2):
    """Decode QR codes in each frame and return times and frame deltas."""
    cap = cv2.VideoCapture(video_path)
    detector = cv2.QRCodeDetector()
    times = []
    deltas = []
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        r1 = frame[roi1[1]:roi1[3], roi1[0]:roi1[2]]
        r2 = frame[roi2[1]:roi2[3], roi2[0]:roi2[2]]
        data1, _, _ = detector.detectAndDecode(r1)
        data2, _, _ = detector.detectAndDecode(r2)
        if data1 and data2:
            deltas.append(int(data2) - int(data1))
            times.append(idx / fps)
        idx += 1
    cap.release()
    return times, deltas


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze frame difference between two QR codes in a video.")
    parser.add_argument("video", help="Input video file")
    parser.add_argument("--fps", type=float, required=True,
                        help="Frame rate of the input video")
    parser.add_argument("--stats", default="stats.txt",
                        help="Output text file with statistics")
    parser.add_argument("--csv", default="delta.csv",
                        help="Output CSV file with time and frame difference")
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.video)
    ret, first_frame = cap.read()
    cap.release()
    if not ret:
        raise RuntimeError("Could not read first frame from video")

    rois = select_rois(first_frame)
    if len(rois) != 2:
        raise RuntimeError("Two regions must be selected")

    times, deltas = analyze(args.video, args.fps, rois[0], rois[1])
    if not deltas:
        raise RuntimeError("No frames with decodable QR codes were found")

    arr = np.array(deltas)
    avg, mn, mx, std = arr.mean(), arr.min(), arr.max(), arr.std()
    with open(args.stats, "w", encoding="utf-8") as f:
        f.write(f"average: {avg}\nmin: {mn}\nmax: {mx}\nstd: {std}\n")

    with open(args.csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "frame_difference"])
        writer.writerows(zip(times, deltas))

    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(times, deltas)
    plt.xlabel("time (s)")
    plt.ylabel("frame difference")
    plt.title("Frame difference vs time")
    plt.show()


if __name__ == "__main__":
    main()
