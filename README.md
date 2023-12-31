# Web Polls for Kasetsart University
[![Django test](https://github.com/Sankrub/ku-polls/actions/workflows/python-app.yml/badge.svg)](https://github.com/Sankrub/ku-polls/actions/workflows/python-app.yml)


An application for conducting a poll or survey with multiple-choice questions, written in Python using Django. It is based on the [Django tutorial project][django-tutorial], and adds additional functionality.

A polls application for [Individual Software Process](https://cpske.github.io/ISP) course at [Kasetsart University](https://ku.ac.th).

## Requirements

Requires Python 3.8 or newer.  Required Python packages are listed in [requirements.txt](./requirements.txt). 

## Install and Configure the Application
[Installation Guide](Installation.md)


## Running the Application (if python doesn't work use python3 instead)
#### Clone repository from github
* ```git clone https://github.com/Sankrub/ku-polls.git```
#### Install Dependencies
* ```pip install -r requirements.txt```
#### Run the server
* ```python manage.py runserver```
#### Go to the browser.
* ```http://localhost:8000```

## Username and Password demo for login
| Username  | Password        |
|-----------|-----------------|
|   demo1   | stupidpassword1 |
|   demo2   | stupidpassword2 |
|   Harry   |    hackme22     |

## Username and Password for admin
| Username  | Password        |
|-----------|-----------------|
|   Harry   |    hackme22     |
## Project Documents


All project-related documents are in the [Project Wiki](../../wiki/Home)

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Development Plan](../../wiki/Development%20Plan)
- [Iteration 1 Plan](../../wiki/Iteration%201%20Plan) and [Task Board](https://github.com/users/Sankrub/projects/1)
- [Iteration 2 Plan](https://github.com/Sankrub/ku-polls/wiki/Iteration-2-plan) and [Task Board](https://github.com/users/Sankrub/projects/1/views/2)
- [Iteration 3 Plan](https://github.com/Sankrub/ku-polls/wiki/Iteration-3-plan) and [Task Board](https://github.com/users/Sankrub/projects/1/views/3)
- [Iteration 4 Plan](https://github.com/Sankrub/ku-polls/wiki/Iteration-4-plan) and [Task Board](https://github.com/users/Sankrub/projects/1/views/4)

[django-tutorial]: https://docs.djangoproject.com/en/3.1/intro/tutorial01/
