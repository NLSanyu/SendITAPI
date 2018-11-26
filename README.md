# SendITAPI
SendIT is a courier service that helps users deliver parcels to different destinations. SendITAPI is the API for this project.


[![Build Status](https://travis-ci.org/NLSanyu/SendITAPI.svg?branch=master)](https://travis-ci.org/NLSanyu/SendITAPI)
[![Coverage Status](https://coveralls.io/repos/github/NLSanyu/SendITAPI/badge.svg?branch=master)](https://coveralls.io/github/NLSanyu/SendITAPI?branch=master)


## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes


### Prerequisites
```
Python 3.6.5
```

### Installation

```
Copy the link for cloning this repository from the "Clone or download button"
Create a folder on your computer
Create a virtual environment and activate it (instructions below are for virtualenvwrapper)
  $ mkvirtualenv my_venv
  $ workon my_venv
Open the terminal or git bash
Enter these commands:
  $ cd YourFolder
  $ git clone <the clone link you copied>
Install the requirements in the requirements.txt file
  $ pip install -r requirements.txt
Set the variable FLASK_APP to "sendit.py" 
  $' set FLASK_APP' (on Windows)  
  $ 'export FLASK_APP' (on Mac)
Run the program:
  $ flask run
Open up your web browser
Go to 127.0.0.1:5000 or localhost:5000 
```


## Running the tests

```
Open the terminal
$ cd YourFolder
$ pytest
```


## Built With
* [Flask](http://flask.pocoo.org/) - The web framework used


## Versioning
Version 1


## Authors

* **Lydia Sanyu Naggayi** 
