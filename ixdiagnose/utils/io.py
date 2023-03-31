import os


def truncate_file(filename: str, max_size: int) -> None:
    size = os.path.getsize(filename)
    if size <= max_size:
        return

    bytes_to_remove = size - max_size
    with open(filename, 'r+b') as f:
        f.seek(bytes_to_remove)
        remaining_contents = f.read()
        f.seek(0)
        f.write(remaining_contents)
        f.truncate(max_size)
