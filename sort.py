import re
from pathlib import Path
import sys

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
folders = list()

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def normalize(name):
    name, extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return f"{new_name}.{extension}"

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in registered_extensions.keys():
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if extension in registered_extensions['IMAGES']:
            image_files_list.append(new_name)
            extensions.append(extension)
        elif extension in registered_extensions['VIDEOS']:
            video_files_list.append(new_name)
            extensions.append(extension)
        elif extension in registered_extensions['DOCUMENTS']:
            document_files_list.append(new_name)
            extensions.append(extension)
        elif extension in registered_extensions['MUSIC']:
            music_files_list.append(new_name)
            extensions.append(extension)
        elif extension in registered_extensions['ARCHIVES']:
            archive_files_list.append(new_name)
            extensions.append(extension)
        else:
            other_files_list.append(new_name)
            unknown_extensions.append(extension)


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    scan(Path(path))

    print(f"image files: {image_files_list}\n")
    print(f"video files: {video_files_list}\n")
    print(f"document files: {document_files_list}\n")
    print(f"music files: {music_files_list}\n")
    print(f"archive files: {archive_files_list}\n")
    print(f"unknown files: {other_files_list}\n")
    print(f"All extensions: {set(extensions)}\n")
    print(f"Unknown extensions: {set(unknown_extensions)}\n")