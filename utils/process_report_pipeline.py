from pathlib import Path


def has_files(directory_path: Path) -> bool:
    # Defensive check: Ensure the path is valid and is actually a directory
    if not directory_path.exists() or not directory_path.is_dir():
        return False

    # Use a generator expression with any() for optimal performance
    return any(item.is_file() for item in directory_path.iterdir())


# --- Example Usage ---
if __name__ == "__main__":
    downloads_dir = Path.home() / "Downloads"

    if has_files(downloads_dir):
        print("Files are present in the directory.")
    else:
        print("The directory is empty or contains only sub-folders.")
