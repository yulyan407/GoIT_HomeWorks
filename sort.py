import re
from pathlib import Path
import sys
import shutil

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

registered_extensions = {'IMAGES': ['JPEG', 'PNG', 'JPG', 'SVG'],
                         'VIDEOS': ['AVI', 'MP4', 'MOV', 'MKV'],
                         'DOCUMENTS': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                         'MUSIC': ['MP3', 'OGG', 'WAV', 'AMR'],
                         'ARCHIVES': ['ZIP', 'GZ', 'TAR'],
                         'OTHERS': []}
unknown_extensions = list()
extensions = list()
image_files_list = list()
video_files_list = list()
document_files_list = list()
music_files_list = list()
archive_files_list = list()
other_files_list = list()

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def normalize(name):
    name, extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return f"{new_name}.{extension}"

def hande_file(file_name, folder, dist):
    target_folder = folder / dist
    target_folder.mkdir(exist_ok=True)
    file_name.rename(target_folder/normalize(file_name.name))

def handle_archive(path, folder, dist):
    target_folder = folder / dist
    target_folder.mkdir(exist_ok=True)

    norm_name = normalize(path.name).replace(".zip", '').replace(".gz", '').replace(".tar", '')

    archive_folder = target_folder / norm_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), archive_folder)
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()

def scan_sort(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in registered_extensions.keys():
                scan_sort(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if extension in registered_extensions['IMAGES']:
            image_files_list.append(new_name)
            extensions.append(extension)
            hande_file(new_name, folder, 'IMAGES')
        elif extension in registered_extensions['VIDEOS']:
            video_files_list.append(new_name)
            extensions.append(extension)
            hande_file(new_name, folder, 'VIDEOS')
        elif extension in registered_extensions['DOCUMENTS']:
            document_files_list.append(new_name)
            extensions.append(extension)
            hande_file(new_name, folder, 'DOCUMENTS')
        elif extension in registered_extensions['MUSIC']:
            music_files_list.append(new_name)
            extensions.append(extension)
            hande_file(new_name, folder, 'MUSIC')
        elif extension in registered_extensions['ARCHIVES']:
            archive_files_list.append(new_name)
            extensions.append(extension)
            handle_archive(new_name, folder, "ARCHIVE")
        else:
            other_files_list.append(new_name)
            unknown_extensions.append(extension)
            target_folder = folder / 'OTHERS'
            target_folder.mkdir(exist_ok=True)
            new_name.rename(target_folder / new_name.name)

def delete_empty_folders(path):
    """
    Delete empty folders
    :param path: user path -> Path
    :return: None
    """
    for item in path.glob('**/*'):
        if item.is_dir():
            try:
                item.rmdir()
            except OSError:
                pass


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    scan_sort(Path(path))

    delete_empty_folders(Path(path))

    print(f"Image files: {image_files_list}\n")
    print(f"Video files: {video_files_list}\n")
    print(f"Document files: {document_files_list}\n")
    print(f"Music files: {music_files_list}\n")
    print(f"Archive files: {archive_files_list}\n")
    print(f"Unknown files: {other_files_list}\n")
    print(f"All extensions: {set(extensions)}\n")
    print(f"Unknown extensions: {set(unknown_extensions)}\n")