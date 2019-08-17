# Mairo to Anki

Mairo to anki is a script to automate phrases synchronization between Mairo Vergara english lessons and Anki platform

## Getting Started

These instructions will get you a copy of the project up and running on your local machine

### Prerequisits

That things you need to run with success this script.

* [Python 3.x](https://www.python.org/downloads/)
* [Anki Desktop](https://apps.ankiweb.net)
* [AnkiConnect](https://ankiweb.net/shared/info/2055492159)

## Usage

Into root project folder at terminal, and execute:

```python
py main.py -u <mairo_username> -p <mairo_password>  -l <[,lesson_ids]> -d <deck_name>
```

Optional parameter:

* **-a <mairo_address_api>** *default: https://curso.mairovergara.com/api/v1/*


## Author

* **Atylla Santos**

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)