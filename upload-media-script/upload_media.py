import os
import re
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

IMAGE_BUCKET = "species_images"
VIDEO_BUCKET = "species_videos"

"REPLACE THESE PATHS WITH YOUR OWN PATHS"
 
IMAGE_FOLDER = Path(
    r"D:\CYN2\Deakin Uni\Deakin T2 Y2\SIT782_TeamProjectB\Species-Database-App\upload-media-script\species_images"
)

VIDEO_FOLDER = Path(
    r"C:\Users\species_videos"
)

OUTPUT_FILE = "uploaded_links.txt"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

uploaded_links = []


def clean_path(path_text):
    path_text = path_text.replace("\\", "/")
    path_text = re.sub(r"\s+", "_", path_text)
    path_text = path_text.replace("(", "").replace(")", "")
    return path_text


def bucket_exists(bucket_name):
    try:
        buckets = supabase.storage.list_buckets()

        for bucket in buckets:
            if bucket.name == bucket_name:
                return True

        return False

    except Exception as e:
        print(f"Failed to check bucket: {bucket_name}")
        print(e)
        return False


def create_bucket_if_missing(bucket_name):
    if bucket_exists(bucket_name):
        print(f"Bucket already exists: {bucket_name}")
        return

    print(f"Creating bucket: {bucket_name}")

    try:
        supabase.storage.create_bucket(
            bucket_name,
            options={"public": True}
        )
        print(f"Created bucket: {bucket_name}")

    except Exception as e:
        print(f"Failed to create bucket: {bucket_name}")
        print(e)
        print("This usually means your SUPABASE_KEY is not the service_role key.")


def list_all_files(bucket_name, folder=""):
    """
    Recursively gets every file inside a Supabase bucket.
    """

    all_files = []

    try:
        items = supabase.storage.from_(bucket_name).list(folder)

        for item in items:
            name = item.get("name")

            if not name:
                continue

            full_path = f"{folder}/{name}" if folder else name

            # If metadata exists, it is usually a file.
            # If not, it is usually a folder.
            if item.get("metadata") is not None:
                all_files.append(full_path)
            else:
                all_files.extend(list_all_files(bucket_name, full_path))

    except Exception as e:
        print(f"Failed to list files in bucket: {bucket_name}/{folder}")
        print(e)

    return all_files


def delete_everything_in_bucket(bucket_name):
    """
    Deletes all existing files in the bucket before reuploading.
    """

    print(f"\nDeleting existing files from bucket: {bucket_name}")

    files = list_all_files(bucket_name)

    if not files:
        print(f"No existing files found in: {bucket_name}")
        return

    try:
        # Delete in chunks to avoid request size issues
        chunk_size = 100

        for i in range(0, len(files), chunk_size):
            chunk = files[i:i + chunk_size]
            supabase.storage.from_(bucket_name).remove(chunk)
            print(f"Deleted {len(chunk)} files...")

        print(f"Finished deleting {len(files)} files from {bucket_name}")

    except Exception as e:
        print(f"Failed deleting files from bucket: {bucket_name}")
        print(e)


def upload_folder(local_folder, bucket_name, allowed_extensions):
    if not local_folder.exists():
        print(f"Folder does not exist: {local_folder}")
        return

    print(f"\nUploading from: {local_folder}")

    for file_path in local_folder.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in allowed_extensions:
            continue

        relative_path = file_path.relative_to(local_folder).as_posix()
        storage_path = clean_path(relative_path)

        try:
            with open(file_path, "rb") as file:
                supabase.storage.from_(bucket_name).upload(
                    path=storage_path,
                    file=file
                )

            public_url = supabase.storage.from_(bucket_name).get_public_url(storage_path)
            uploaded_links.append(public_url)

            print(f"Uploaded: {file_path}")
            print(f"URL: {public_url}")
            print("-" * 60)

        except Exception as e:
            print(f"Failed: {file_path}")
            print(e)
            print("-" * 60)


def save_links_to_file():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("UPLOADED MEDIA LINKS\n")
        file.write("=" * 80 + "\n\n")

        for link in uploaded_links:
            file.write(link + "\n")

    print(f"\nSaved links to: {OUTPUT_FILE}")


def main():
    print("Starting uploader...\n")

    create_bucket_if_missing(IMAGE_BUCKET)
    create_bucket_if_missing(VIDEO_BUCKET)

    delete_everything_in_bucket(IMAGE_BUCKET)
    delete_everything_in_bucket(VIDEO_BUCKET)

    print("\n=== UPLOADING IMAGES ===")
    upload_folder(
        IMAGE_FOLDER,
        IMAGE_BUCKET,
        IMAGE_EXTENSIONS
    )

    print("\n=== UPLOADING VIDEOS ===")
    upload_folder(
        VIDEO_FOLDER,
        VIDEO_BUCKET,
        VIDEO_EXTENSIONS
    )

    save_links_to_file()

    print("\nFinished deleting old media and reuploading everything.")


if __name__ == "__main__":
    main()