# SanktGallenBot
SanktGallenBot is a user friendly way to make open data accessible to everyone through telegram. It was initially created as part of the [Open Data Hack St.Gallen 2021](telegram.me/SanktGallenBot). We aim to create a developer and contribution friendly environment to be able to integrate further data sets quickly.

https://opendata-hack-stgallen.devpost.com/
[SanktGallenBot](telegram.me/SanktGallenBot)

## Features
- Find nearest carpark
- Find nearest collection point
- Find nearest charging station
- Receive notifications for cardboard and paper disposal

## Contribute
Want to contribute? Great!

Contributions are more then welcome. Please follow the structure of the project. Features stored in their own subfolders within the main directory. These features may only access themselves and the common directory. The handlers must be initialised in main.py. Schedulers such as notify.py must also be created in the main directory.

Don't hesistate to open an issue or a pull request.

## Dev Setup
- Install Python3
- Install Pip3
- Run pip install -r requirements.txt
- Create mysql database and run it on port 3306
- Create Database and tables according to createDatabase.sql in the main folder
- [Create a new telegram bot and generate a token](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token)
- Set data access information and newly created token in config.json
