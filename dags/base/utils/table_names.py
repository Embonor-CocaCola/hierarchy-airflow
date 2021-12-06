from const.constants import RAW_SUFFIX, TMP_PREFIX
from const.table_name_maps import original_table_name_to_new_name_map


class TableNameManager:
    def __init__(self, original_names: list[str]):
        if not original_names:
            raise ValueError('Missing parameter original_names')

        self.__original_names = original_names
        self.__table_names = {}

        for name in original_names:
            self.__table_names[name] = {'original': name, 'normalized': None, 'raw': None, 'tmp': None}

    def get_variations(self, table_name: str):
        self.__load_name_variants(table_name)
        return self.__table_names[table_name]

    def get_original_names(self) -> list:
        return self.__original_names

    @staticmethod
    def append(table_name: str, suffix: str) -> str:
        return f'{table_name}{suffix}'

    def __create_raw_table_name(self, table_name: str):
        return self.append(self.__normalized(table_name), RAW_SUFFIX)

    def __create_tmp_table_name(self, table_name: str):
        return self.append(TMP_PREFIX, self.__normalized(table_name))

    def __load_name_variants(self, table_name: str) -> None:
        self.__raw(table_name)
        self.__tmp(table_name)

    def __normalized(self, original_name: str) -> str:
        if not self.__table_names[original_name]['normalized']:
            self.__table_names[original_name]['normalized'] = original_table_name_to_new_name_map[original_name]
        return self.__table_names[original_name]['normalized']

    def __raw(self, original_name: str) -> None:
        if not self.__table_names[original_name]['raw']:
            self.__table_names[original_name]['raw'] = self.__create_raw_table_name(original_name)

    def __tmp(self, original_name: str) -> None:
        if not self.__table_names[original_name]['tmp']:
            self.__table_names[original_name]['tmp'] = self.__create_tmp_table_name(original_name)
