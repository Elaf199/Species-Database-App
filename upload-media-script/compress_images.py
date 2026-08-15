import os
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

INPUT_FOLDER = "input_images"
OUTPUT_FOLDER = "optimized_images"

MAX_SIZE = (1600, 1600)  # set to None to disable resizing
WEBP_QUALITY = 80


def format_size(num_bytes):
    if num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.1f} KB"
    return f"{num_bytes / (1024 * 1024):.2f} MB"


def process_image(input_path, output_path):
    try:
        with Image.open(input_path) as img:

            # Ensure correct mode
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA" if "A" in img.getbands() else "RGB")

            # Resize if needed
            if MAX_SIZE is not None:
                img.thumbnail(MAX_SIZE)

            # Change extension to .webp
            output_path = os.path.splitext(output_path)[0] + ".webp"

            # Save compressed
            img.save(output_path, "WEBP", quality=WEBP_QUALITY, optimize=True)

        original_size = os.path.getsize(input_path)
        new_size = os.path.getsize(output_path)
        saved = 100 * (original_size - new_size) / original_size if original_size > 0 else 0

        print(f"Done: {input_path}")
        print(f"  Original:  {format_size(original_size)}")
        print(f"  Optimized: {format_size(new_size)}")
        print(f"  Saved:     {saved:.1f}%\n")

    except Exception as e:
        print(f"Failed: {input_path} -> {e}")


def main():
    if not os.path.exists(INPUT_FOLDER):
        print(f"Input folder '{INPUT_FOLDER}' does not exist.")
        return

    for root, dirs, files in os.walk(INPUT_FOLDER):
        for file in files:
            if not file.lower().endswith((".jpg", ".jpeg", ".png", ".heic", ".heif")):
                continue

            input_path = os.path.join(root, file)

            # Create matching output path
            relative_path = os.path.relpath(input_path, INPUT_FOLDER)
            output_path = os.path.join(OUTPUT_FOLDER, relative_path)

            # Ensure subfolder exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            process_image(input_path, output_path)

    print("Finished processing all images.")


if __name__ == "__main__":
    main()