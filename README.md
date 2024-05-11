# Mic Plot Generator

A Django-based web application to render mic plots.

## Usage

**Setup**

NOTE: when running any commands, you need to make sure to have the virtual environment enabled by first running `env.bat` (the venv is created when running `setup.bat`, see below). To make this easier, open terminal and navigate to the root directory, then type in `env.bat` to load the environment, and subsequently run any other batch files the same way.

To setup the environment, run `setup.bat`, or open terminal and run the following commands
```console
py -m venv .venv
env.bat
pip install -r requirements.txt
echo SECRETKEY='INSECURE-CHANGE' >> .env
py -m manage makemigrations micplot
py -m manage sqlmigrate micplot 0001
py -m manage migrate
```

[Expected command output](#setup-commands-output)

Use `run.bat` to launch the django server on `127.0.0.1:8000`

**Web-based database management**

To allow you to edit the database via the `/admin` page, you will need to setup a superuser using `python manage.py createsuperuser` and follow the instructions. Open the local domain - e.g. (http://127.0.0.1:8000/admin/), where you can then edit database values. ONLY DO THIS IF YOU KNOW WHAT YOU'RE DOING. To view the model syntax, [see below](#model-syntax).

## Deployment

**Preparing settings for deployment**

To deploy the system, first go to `\main\settings.py` and update the following variables
```python
debug = False
```
and generate a secure secret key for the `.env` file by using `generate_secret_key.py`

**Collecting static files**

Run `collectstatic.bat`, or open terminal and run this command. If prompted, confirm by entering `yes`.
```console
python -m manage collectstatic
```

This will generate a `\static\` directory in the root directory, which will contain all of the static files for the program.

The program is now ready to be run! (See [Usage](#usage) for information on how to run).
For website hosting, I'd recommend using [railway.app](https://railway.app/) and linking it to a git deployment branch.

## Model Syntax

--- NEED TO ADD ---

## Methodology

--- NEED TO ADD ---

## Setup Commands Output

```console

```

```console

```