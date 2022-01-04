# YRAP - Your Routines and Projects

## What Is YRAP All About

This project is very personal, and so it's usage may not be useful to most people.  However,
you'd probably be able to adapt it to your use case provided you know a bit of Python.

The idea is to have an interface which provides a service to manage projects and routines
in one place.  The projects idea is based on the popular book ["Getting Things Done"][GTD] by
David Allan.


## Requirements

The server a docker compose project, and so having docker installed and a good
internet connection are really the only requirements to run the server.

The server uses:
- Python >= 3.9
- Django
- Django Rest Framework
- postgresql

The command line client requires:

The command line client uses the following:
- Python >= 3.9
- Poetry
- Requests


## Installation

1. Decide where to place the project and cd to that directory
    `$ cd /path/to/root/dir`

2. Clone the repo
    `$ git clone https://github.com/namibnat/yrap.git`



## Usage

### Website and Server


Build and run the server (This could be moved to a server, but for dev, just on your local)
    `$ cd server/yrap_server`

Create a secrete key (You can use [[djecrety.ir]][[djecrety.ir]]).  Create a .env file
in the root directory of the django project (the same one that has the manage.py file), and
add the line:
    `SECRETE_KEY='....your secret key...'`

To the same file, add your postgres database password, the same as you use in the compose file.
    `PASSWORD='...your password...'`

Now you can build and run your server:
    `$ docker compose up --build -d`

The terminal based client is purely a command line app
    `$ cd ../cmd_client`
    `$ poetry shell`

For now, this is the only aspect of the project that works unless you've changed it.
The server runs a web interface, which is at your localhost:8000.

Click on the menu to go to projects.

The go to the command line.  See the options with:
    `$ python project --help`

Add a new project with:
    `$ python project --add`


## Documentation

These will be provided in the "docs" folder when they are required.


## Tests

For now, the tests just run the basic python unittest module.

Run:
`$ python -m unittest discover`


## License

YRAP is licensed under the terms of the MIT License (see the file LICENSE).


## Contributing

I would be thrilled if some programmers from the Python Namibia community contribute.  But, if you're
a python developer and see some use to the project in your own work, please feel free to send a pull request.


[GTD]: https://gettingthingsdone.com/
[djecrety.ir]: https://djecrety.ir/