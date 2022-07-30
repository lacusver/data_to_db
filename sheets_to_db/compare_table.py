class TableCompare():

    @classmethod
    def get_rows_indx_to_delete(cls, row_db_dict, row_sheet_dict):
        # формируем список индексов на удаление, берем индексы которые встречаются только в бд
        indx_del = row_db_dict.keys() - row_sheet_dict.keys()
        return tuple(indx_del)
    
    @classmethod
    def get_rows_to_add(cls, row_db_dict, row_sheet_dict):
        # формируем список на добавление, берем только те значения, индексы которых есть только в google sheet
        rows_new = [row_sheet_dict.get(key) for key in row_sheet_dict.keys() - row_db_dict.keys() if len(row_sheet_dict.get(key))==4]
        return rows_new
    
    @classmethod
    def get_rows_to_update(cls, row_db_dict, row_sheet_dict):
        # формируем список на обновление, берем значения, индексы которых встречаются в обоих таблицах
        rows_update = [row_sheet_dict.get(key) for key in row_sheet_dict.keys() & row_db_dict.keys()]
        return rows_update
    
    @classmethod
    def create_row_dict(cls, lst):
        # создание словаря, ключ - индексы в таблце
        # значения - поля в таблице
        row_dict = {x[0]:x for x in lst}
        return row_dict

    @classmethod
    def get_rows(cls, row_db, row_sheet):
        lst_db_diff = set(row_db) - set(row_sheet) # получаем поля, которые должны быть изменены или удалены в бд
        lst_sheet_diff = set(row_sheet) - set(row_db) # поля, которые изменены или которые нужно добавить
        row_db_dict = cls.create_row_dict(lst_db_diff) # формируем из полученных значений два словаря,
                                                        # ключами будут индексы из таблиц
                                                        # нужно, чтобы разграничить поля на удаление и изменение
        row_sheet_dict = cls.create_row_dict(lst_sheet_diff)
        
        rows_to_add = cls.get_rows_to_add(row_db_dict, row_sheet_dict) # получаем поля на доб-ие, обнов-ие и удаление
        rows_to_update = cls.get_rows_to_update(row_db_dict, row_sheet_dict)
        rows_indx_delete = cls.get_rows_indx_to_delete(row_db_dict, row_sheet_dict)

        return (rows_to_add, rows_to_update, rows_indx_delete) # возвращаем кортеж из списков полей на обработку бд