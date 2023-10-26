import os
from abc import ABC, abstractmethod


class Specification(ABC):
    """Abstract class for specifications"""

    @abstractmethod
    def is_satisfied(self, item: list) -> bool:
        pass

    def __and__(self, other):
        """Overload the & operator to check if all specifications are satisfied"""
        return AndSpecification(self, other)

    def __or__(self, other):
        """Overload the | operator to check if any specification is satisfied"""
        return OrSpecification(self, other)

    def __invert__(self):
        """Overload the ~ operator to check if any specification is satisfied"""
        return NotSpecification(self)


class AndSpecification(Specification):
    """Class for and specifications"""

    def __init__(self, *args) -> None:
        self.args = args

    def is_satisfied(self, item: dict) -> bool:
        return all(spec.is_satisfied(item) for spec in self.args)


class OrSpecification(Specification):
    """Class for or specifications"""

    def __init__(self, *args) -> None:
        self.args = args

    def is_satisfied(self, item: dict) -> bool:
        return any(spec.is_satisfied(item) for spec in self.args)


class NotSpecification(Specification):
    """Class for not specifications"""

    def __init__(self, spec) -> None:
        self.spec = spec

    def is_satisfied(self, item: dict) -> bool:
        return not self.spec.is_satisfied(item)


class Filter(ABC):
    """Abstract class for filters"""

    @abstractmethod
    def filter(self, item: dict, spec: Specification) -> object:
        """Abstract method for filtering"""
        pass


class FileName(Specification):
    """Class for file name specifications"""

    def __init__(self, *args) -> None:
        self.file_names = args

    def is_satisfied(self, item: dict) -> bool:
        item_file_names = item['file_name'].lower()
        for file_name in self.file_names:
            if file_name in item_file_names:
                return True


class FolderNames(Specification):
    """Class for folder name specifications"""

    def __init__(self, *args) -> None:
        self.folder_name = args

    def is_satisfied(self, item: dict) -> bool:
        item_folder_names = [x.lower() for x in item['folder_names']]
        if any(x in y for x in self.folder_name for y in item_folder_names):
            return True


class Extension(Specification):
    """Class for extension specifications"""

    def __init__(self, *args) -> None:
        self.extension = args

    def is_satisfied(self, item: dict) -> bool:
        item_extension = item['extension'].lower()
        for extension in self.extension:
            if extension in item_extension:
                return True


class SubjectFilter(Filter):
    """Class for filtering items"""

    def filter(self, items: list, spec: Specification) -> dict:
        count = 0
        for item in items:
            if spec.is_satisfied(item):
                count += 1
                yield item
        print(f'found {count} files')


class RecursiveFileLister:
    """Class for extracting file paths from a directory"""

    def __init__(self, path: str) -> None:
        self.path = path

    def __call__(self) -> list[dict]:
        """Extract all file paths from a directory"""
        file_paths = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file_paths.append(os.path.join(root, file))

        file_paths.sort()

        extracted_paths = []
        for file_path in file_paths:
            extracted_paths.append(self.extract_file_info(file_path))
        return extracted_paths

    @staticmethod
    def extract_file_info(file_path: str) -> dict:
        """Extract file name, folder names and extension from a file path"""
        file_name = os.path.basename(file_path)
        file_base_name, extension = file_name.split('.', 1)
        folder_names = os.path.dirname(file_path).split(os.path.sep)  #
        folder_names = [x for x in folder_names if x]  # remove empty strings
        item = {
            'file_path': file_path,
            'file_name': file_name,
            'extension': extension,
            'file_base_name': file_base_name,
            'folder_names': folder_names,
        }
        return item


if __name__ == '__main__':

    src = '/home/*path*/huge_mess'
    dst = '/home/*path*/clean_stuff'

    os.makedirs(dst, exist_ok=True)

    rfl = RecursiveFileLister(src)
    extracted_files = rfl()

    sf = SubjectFilter()

    # Define the specifications for filtering with binary operators (&, |, ~) and FileName, FolderNames and Extension
    for subject in sf.filter(extracted_files,
                             FileName('my_special_name') |
                             FileName('second_special_name') &
                             ~FileName('this_is_bad_data') &
                             FolderNames('my_folder_name', 'sometimes_this_name') &
                             Extension('img', 'jpg')):

        print(f'process -> {subject["file_path"]}')
