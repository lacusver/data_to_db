import time
from sheets_to_db.main_driver import MainDriver


while True:
    MainDriver.start_app()
    time.sleep(5)