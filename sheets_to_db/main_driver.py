"""
    1. Проверяем существание бд, если нет -> создаем
    2. Проверяем существование таблицы, если нет -> создаем
    3. Проверяем revision таблицы из google disk, если были измения:
        1.1 получаем данные из google sheets
        1.2 получаем из бд
        1.3 сравниваем данные из таблиц, получаем поля на удаление, обновление, редактирование
        1.4 обновляем бд
    4. Проверяем exchange_rate, если день обновился, то загружаем информацию о курсе из ЦБ 
        и обновляем колонку price_ru

"""
import sheets_to_db.exchange_rate as exchange_rate
import sheets_to_db.postg_db_driver as postg_db_driver
import sheets_to_db.google_api_driver as google_api_driver
import sheets_to_db.compare_table as compare_table
import sheets_to_db.telegram_push as telegram_push
import sheets_to_db.delivery_date_expire as delivery_date_expire

class MainDriver():

    @classmethod
    def start_app(cls):
        postg_db_driver.Database.create_database()
        postg_db_driver.Database.connect_to_db()
        postg_db_driver.Database.create_table()

        if google_api_driver.GoogleDriver.check_new_revisions(): # проверяем были ли измения в таблицы, получая время последних изменений
            rows_db = postg_db_driver.Database.get_data() #получаем список записей из бд
            rows_sheet = google_api_driver.GoogleDriver.get_data() #получаем список записей из google_sheet
            rows_to_add, rows_to_update, rows_indx_delete = compare_table.TableCompare.get_rows(rows_db, rows_sheet)
            # получаем список записей на добавление, обновление, и список индексов на удаление, 
            # если не пустые, обновляем данные в бд 
            if rows_to_add:
                postg_db_driver.Database.add_new_data(rows_to_add)
            if rows_to_update:
                postg_db_driver.Database.update_data(rows_to_update)
            if rows_indx_delete:
                postg_db_driver.Database.delete_rows(rows_indx_delete)
        
        if exchange_rate.ExchangeRate.check_new_exchange_date(): # проверяем не обновился ли день -> обновляем колонку с ценной в рублях
            postg_db_driver.Database.update_price()
        
        rows_to_send = delivery_date_expire.DeliveryExpire.check_delivery_date()
        if rows_to_send:
            telegram_push.TelegramBot.send_message(rows_to_send)