from datetime import datetime
import pytz
import sheets_to_db.postg_db_driver as postg_db_driver

class DeliveryExpire:
    rows_indx_sent = []
    new_day_check = None

    @classmethod
    def check_row(cls, row, td):
        return row[0] not in cls.rows_indx_sent and datetime.date(datetime.strptime(row[-1], "%d.%m.%Y")) < td

    @classmethod
    def get_rows_to_send(cls, row):
        cls.rows_indx_sent.append(row[0])
        return f"order_id: {row[1]} price, $: {row[2]} date: {row[-1]}"       
    
    @classmethod
    def check_delivery_date(cls):
        expired_delivery_rows = None
        today_date = datetime.now(pytz.timezone('Europe/Moscow')).date()
        if cls.new_day_check != today_date:
            cls.new_day_check = today_date
            rows = postg_db_driver.Database.get_data()
            if len(rows)!=0:
                expired_delivery_rows = '\n'.join([cls.get_rows_to_send(row) for row in rows if cls.check_row(row, today_date)])
        return expired_delivery_rows