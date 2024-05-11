# Mic Plot Generator

A Django-based web application to render mic plots.

## Usage

**Setup**

NOTE: when running any commands, you need to make sure to have the virtual environment enabled by first running `env.bat` (the venv is created when running `setup.bat`, see below). To make this easier, open terminal and navigate to the root directory, then type in `env.bat` to load the environment, and subsequently run any other batch files the same way.

To setup the environment, run `setup_p1.bat`, or open terminal and run the following commands
```console
py -m venv .venv
env.bat
```

Then run `setup_p2.bat`, or open terminal and run the following commands
```console
py -m pip install -r requirements.txt
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

C:\...\MicPlot>setup_p1.bat

C:\...\MicPlot>py -m venv .venv

C:\...\MicPlot>env.bat

C:\...\MicPlot>.venv\Scripts\activate.bat

```

```console

(.venv) C:\...\MicPlot>setup_p2.bat

(.venv) C:\...\MicPlot>py -m pip install -r requirements.txt 

... INSTALLS LIBRARIES HERE ... 

Successfully installed Django-4.2.13 asgiref-3.8.1 beautifulsoup4-4.12.3 django-bootstrap-v5-1.0.11 python-dotenv-1.0.1 soupsieve-2.5 sqlparse-0.5.0 tzdata-2024.1 whitenoise-6.6.0

(.venv) C:\...\MicPlot>echo SECRETKEY='INSECURE-CHANGE'  1>>.env 

```

```console

(.venv) C:\...\MicPlot>py -m manage makemigrations micplot       
Migrations for 'micplot':
  micplot\migrations\0001_initial.py
    - Create model Act
    - Create model Mic
    - Create model Show
    - Create model Scene
    - Create model MicPos
    - Add field show to mic
    - Add field show to act

```

```console

(.venv) C:\...\MicPlot>py -m manage sqlmigrate micplot 0001 
BEGIN;
--
-- Create model Act
--
CREATE TABLE "micplot_act" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "created" datetime NOT NULL, "updated" datetime NOT NULL);
--
-- Create model Mic
--
CREATE TABLE "micplot_mic" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "packnumber" integer NOT NULL, "mixchannel" integer NOT NULL, "created" datetime NOT NULL, "updated" datetime NOT NULL);
--
-- Create model Show
--
CREATE TABLE "micplot_show" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "date" date NULL, "created" datetime NOT NULL, "updated" datetime NOT NULL);
--
-- Create model Scene
--
CREATE TABLE "micplot_scene" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "number" integer NOT NULL, "created" datetime NOT NULL, "updated" datetime NOT NULL, "act_id" bigint NOT NULL REFERENCES "micplot_act" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model MicPos
--
CREATE TABLE "micplot_micpos" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "actor" varchar(100) NOT NULL, "speaking" integer NOT NULL, "created" datetime NOT NULL, "updated" datetime NOT NULL, "mic_id" bigint NOT NULL REFERENCES "micplot_mic" ("id") DEFERRABLE INITIALLY DEFERRED, "scene_id" bigint NOT NULL REFERENCES "micplot_scene" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field show to mic
--
CREATE TABLE "new__micplot_mic" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "packnumber" integer NOT NULL, "mixchannel" integer NOT NULL, "created" datetime NOT NULL, "updated" datetime NOT NULL, "show_id" bigint NOT NULL REFERENCES "micplot_show" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__micplot_mic" ("id", "packnumber", "mixchannel", "created", "updated", "show_id") SELECT "id", "packnumber", "mixchannel", "created", "updated", NULL FROM "micplot_mic";
DROP TABLE "micplot_mic";
ALTER TABLE "new__micplot_mic" RENAME TO "micplot_mic";
CREATE INDEX "micplot_scene_act_id_32c17705" ON "micplot_scene" ("act_id");
CREATE INDEX "micplot_micpos_mic_id_2ba8c921" ON "micplot_micpos" ("mic_id");
CREATE INDEX "micplot_micpos_scene_id_2df63678" ON "micplot_micpos" ("scene_id");
CREATE INDEX "micplot_mic_show_id_b887615b" ON "micplot_mic" ("show_id");
--
-- Add field show to act
--
CREATE TABLE "new__micplot_act" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "created" datetime NOT NULL, "updated" datetime NOT NULL, "show_id" bigint NOT NULL REFERENCES "micplot_show" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__micplot_act" ("id", "name", "created", "updated", "show_id") SELECT "id", "name", "created", "updated", NULL FROM "micplot_act";
DROP TABLE "micplot_act";
ALTER TABLE "new__micplot_act" RENAME TO "micplot_act";
CREATE INDEX "micplot_act_show_id_c0ef2806" ON "micplot_act" ("show_id");
COMMIT;

```

```console

(.venv) C:\...\MicPlot>py -m manage migrate 
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, micplot, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying micplot.0001_initial... OK
  Applying sessions.0001_initial... OK

(.venv) C:\...\MicPlot>

```