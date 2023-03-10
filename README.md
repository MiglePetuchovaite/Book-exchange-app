# Book-exchange-app

Book exchange app - the book-swapping platform where you can give away the books you no longer need and exchange them for the ones you want to read. 

![image](https://user-images.githubusercontent.com/105554616/224053688-0e919cc1-d8b1-404c-9baf-ddcbf037917d.png)


# Getting Started

# Installation

First, you need to clone this repository in Sourcetree:

git clone git@github.com:MiglePetuchovaite/Book-exchange-app.git

Or:

git clone https://github.com/MiglePetuchovaite/Book-exchange-app.git

Then choose folder where to save in your computer:

![image](https://user-images.githubusercontent.com/105554616/224057581-8aad90c6-7ce5-42e8-965c-685a404b2d03.png)

Now, we will need to create a virtual environment and install all the dependencies:

On Windows, terminal bash:  python -m venv venv

and copy thhis to activate vnv: venv\Scripts\activate

Install all requiriments from requiriments file:

pip install -r requirements.txt

How to Run application

To run application stand onrun.py file and press Run Python File (right coner in Visual Studio Code)

Software dependencies:

Run (/run.py): Run app with Flask.

Init (/__init__.py): It contains the application factory.

Templates (/templates): Templating with Flask and Jinja2.

Forms (/forms.py): Form handing with Flask-WTF (WTForms), File upload and integrating with FileField, FileAllowed.

Database (/book.db): Database with Flask-SQLAlchemy (SQLAlchemy).

Models (/models.py): Declaring models with sqlalchemy.

Utils (/utils.py): Saving uploded picture with Flask-Pillow.

views (/views.py): Handeling URL request with code.

Static (/images): Images filing with Flask-Pillow.

# Built With:

Python-Flask, SQL, Bootstrap.
