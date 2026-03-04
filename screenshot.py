import mss
import os

# Ensure output directory exists
output_dir = "/Users/konglingzheng/.openclaw/workspace"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "screenshot.png")

with mss.mss() as sct:
    screenshot = sct.shot(output=output_path)
    print(f"Screenshot saved to {screenshot}")
