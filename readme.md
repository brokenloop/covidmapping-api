# CovidMapping API

This project stores, updates, and delivers data about the spread of COVID-19, as collected by [/r/covidmapping](reddit.com/r/covidmapping).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You must have Python 3.7 or above installed on your machine.

### Installing

We recommend that you use a virtual environment when working with this project.

```
python3 -m venv env
source env/bin/activate
```

#### Install dependencies

```
pip install -r requirements.txt
```

#### Setup Database
```
python manage.py makemigrations
python manage.py migrate
```

#### Run the project! 
```
python manage.py runserver
```

Now you should be able to visit http://localhost:8000, and you'll have your API up and running! 

## Contributing

We're actively looking for contributors!

## Authors

* **Daniel Jordan** - *Initial work* - [brokenloop](https://github.com/brokenloop)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Shoutout to everyone at /r/covidmapping for collecting such a wide array of data.
