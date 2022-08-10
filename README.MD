## Transfer Google Sheets data to PostgreSQL using Google API
Python script can track changes in Google Sheets and update data in the database.
* You can `update/delete/add` rows in google sheets file, script will automatically update db in postgres.
* Script sends a message to telegram bot if delivery date is expired.
* Script daily gets current exchange rate from the [central bank](http://www.cbr.ru/development/sxml/) and update column price_rub.
## Instructions for running the script:
1. Clone the repository: `git clone` .
2. Install all requirements `pip install -r requirements.txt`.
3. Make a copy of [the file in Google Sheets](https://docs.google.com/spreadsheets/d/15OFkjwQBcMkX40YDCZB03pHGQqvOh1dBsPnbTAyFhEs/edit?usp=sharing).
4. Create a project in Google Cloud Platform.
5. Add Sheets API to your project.
6. Create a service account and get a json format file with service account key.
7. Add your service account email to your copy of  google sheets file as Viewer.
8. Place your service account key in the `creds/creds_api.json` file.
9. Set the necessary parameters in the config file:
   + postgresql db settings
   + google sheets id
   + your telegram bot settings (token, chat_id)
10. Run script main.py, it will create a db and a table for it. It will track changes in Google Sheets using revision history of the file. 
