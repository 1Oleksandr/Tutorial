import sys
import os
import shutil


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

type_of_file = {'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
                'video': ('AVI', 'MP4', 'MOV', 'MKV'),
                'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
                'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'PY'),
                'archives': ('ZIP', 'GZ', 'TAR')}


def normalize(name):

    translate_name = name.translate(TRANS)
    normalize_name = ''
    for letter in translate_name:
        if not ('a' <= letter <= 'z' or 'A' <= letter <= 'Z' or '0' <= letter <= '9' or letter == '.'):
            normalize_name += '_'
        else:
            normalize_name += letter
    return normalize_name


def parse_args():
    path = ''
    if len(sys.argv) == 1:
        path = os.getcwd()
        print('Обробляємо поточну теку!')
    else:
        path = sys.argv[1]
        print(f'Обробляємо теку - {path}')
    return path


def compare_type_of_file(ext, type_file='unknown'):
    know_file = False
    for type_file, extension in type_of_file.items():
        for el in extension:
            if ext == el:
                know_file = True
                return know_file, type_file
        type_file = 'unknown'
    return know_file, type_file


# если название директории совпадает с именем ключа в словаре -
# удаляем из списка директорий - они не обрабатываются
def compare_types(list_dir):
    for i in type_of_file.keys():
        if i in list_dir:
            list_dir.remove(i)
    return list_dir


def parse(path, files=[]):
    for i in os.listdir(path):
        if os.path.isdir(os.path.join(path, i)):
            if i == 'unknown':
                print(
                    f'Не обрабатываем папку {os.path.join(path, i)} т.к. этот тип папки не обрабатывается\n')
                continue
            if i in type_of_file:
                print(
                    f'Не обрабатываем папку {os.path.join(path, i)} т.к. этот тип папки не обрабатывается\n')
            else:
                parse(os.path.join(path, i), files)
        else:
            files.append(os.path.join(path, i))
    return files


def sort_files(files, our_root_path):
    know_ext = set()
    list_files_by_category = {}
    for i in files:
        cur_file = os.path.split(i)  # вычленяем имя файла
        # вычленяем имя и расширение файла
        div_file_ext = os.path.splitext(cur_file[1])
        know_file, type_file = compare_type_of_file(
            div_file_ext[1][1:].upper())
        type_file_dir = os.path.join(our_root_path, type_file)

        if not know_file:
            if not 'unknown' in type_of_file:
                type_of_file['unknown'] = list()
            if not div_file_ext[1][1:].upper() in type_of_file:
                type_of_file['unknown'].append(div_file_ext[1][1:].upper())
        else:
            know_ext.add(div_file_ext[1][1:].upper())

        if not type_file in list_files_by_category:
            list_files_by_category[type_file] = list()
        list_files_by_category[type_file].append(i)

        if not os.path.exists(type_file_dir):
            os.mkdir(type_file_dir)
        if type_file == 'archives':
            path_unpack_arch = os.path.join(
                our_root_path, type_file, div_file_ext[0])
            print(f'Файл: {i} распаковываем в {path_unpack_arch}\n')
            os.mkdir(path_unpack_arch)
            shutil.unpack_archive(i, path_unpack_arch)
            os.remove(i)
        else:
            print(f'Файл: {i} перемещаем в {type_file}\n')
            os.rename(i, os.path.join(type_file_dir, normalize(
                div_file_ext[0]) + div_file_ext[1]))

    return type_of_file, know_ext, list_files_by_category


def del_empty_dirs(path):
    list_dir = os.listdir(path)
    list_dir = compare_types(list_dir)
    for j in list_dir:
        for i in list_dir:
            path_dir = os.path.join(path, i)
            if os.path.isdir(path_dir):
                print(path_dir, len(os.listdir(path_dir)))
                if len(os.listdir(path_dir)) == 0:
                    os.rmdir(path_dir)
                    print(f'Пустая папка {path_dir}. Удаляем ее\n')
                    del_empty_dirs(path)
                else:
                    del_empty_dirs(path_dir)


def main():
    path = parse_args()
    if not os.path.exists(path):
        print(f'{path} - такої теки не існує!')
        return "Folder dos not exists"
    our_root_path = path
    list_files = parse(path, [])
    type_of_file, know_ext, list_files_by_category = sort_files(
        list_files, our_root_path)
    del_empty_dirs(our_root_path)
    print(
        f'Результат работы программы в файле {os.path.join(our_root_path, "sort.log")}')
    with open(os.path.join(path, 'sort.log'), "w") as fh:
        fh.write(
            f'Cписок всех файлов в обрабатываемой директории со всеми вложенными директориями:\n {list_files} \n')
        if not 'unknown' in type_of_file:
            fh.write(
                f'Не найдены файлы неизвестных типов\n')
        else:
            fh.write(
                f'Найдены следующие неизвестные типы файлов : {type_of_file["unknown"]}\n')
        if not know_ext:
            fh.write(
                f'Не найдены известные типы файлов\n')
        else:
            fh.write(
                f'Найдены следующие известные типы файлов : {know_ext}\n')
        fh.write(
            f'Cписок файлов по категориям: \n')
        for cat, list_file in list_files_by_category.items():
            fh.write(f'{cat} : {list_file}\n')


if __name__ == '__main__':

    main()
