import os

def scan_directory(directory):
    """Scans the given directory and returns a list of all files and subdirectories."""
    items = []
    for root, dirs, files in os.walk(directory):
        for name in dirs:
            items.append(os.path.join(root, name))
        for name in files:
            items.append(os.path.join(root, name))
    return items

if __name__ == "__main__":
    directory_path = "/Users/bobo/Developer/se-flow-agent/data/books/"  # Replace with your directory path
    all_items = scan_directory(directory_path)

    types = set()
    for item in all_items:
        types.add(item.split('.')[-1] if '.' in item else 'directory')
    print("Found types:", types)