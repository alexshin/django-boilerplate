# Overview

This django boilerplate had been done to solve some routine with creating new environment, installing based batteries 
etc.

## Specifics

It's used some specifics tools to make your programming process easier.

##### Docker and docker-compose

In the root of project you can find `docker-compose.yaml` which contains some containers with databases.

All credentials which is used in development process are open and they are in docker-compose.yaml and
in dev/test settings. For production purposes I recommend to use System Environment Variables or 
some secure tools sush as Hashi Corp Vault etc.

##### Dependencies

All needed dependencies are in the root directory in file `requirements.txt`. If you will change some versions, 
please don't forget to launch tests.

##### Environment settings

Boilerplate contains three different environments:

* _Development_ - not-encrypted credentials, debug tools, api documentation etc.
* _Testing_ - it's the same as Development except debug tools and other redundant apps
* _Production_ - boilerplate doesn't contain ready to use settings cause you _REALLY NEED TO DO IT YOURSELF_

## Additional batteries

#### Django-channels

Recently almost all the projects should use realtime communication between client and server. In this case there 
are not a lot of options. Django-channels enable you to use web-sockets as simple as possible.

**Pay attention on** that you should use Daphne application server against familiar ones: uwsgi or gunicorn.

Check more detail information in [documentation of django-channels](http://channels.readthedocs.io/en/latest/)

#### Django-guardian

This battery allows you to use Object-Level-Permissions against Class-Level-Permissions which exists in Django by 
default.

If you don't know about Django-guardian, you should check 
[the documentation](https://django-guardian.readthedocs.io/en/stable/) ASAP. It will help you in every application
you will create on Django.

#### drf-yasg

Yet another swagger generator helps to generate OpenAPI schema and viewer for Django Rest Framework views. See more 
docs in [official documentation](https://drf-yasg.readthedocs.io/en/stable/index.html)

_In dev environment you can check schema by `http://127.0.0.1:8000/swagger/` or `http://127.0.0.1:8000/redoc/`_

#### django-cors-headers

Added headers to enable CORS. For more information see 
[official documentation](https://github.com/ottoyiu/django-cors-headers/)

## Usage

### Requirements

* Python 3.7
* Docker and Docker-compose (min version of Docker-compose format is 3.1)


### Quick start

```bash
# Create project directory
mkdir -p ./Projects/new-project && cd ./Projects/new-project

# Clone this repository
git clone git@github.com:alexshin/django-boilerplate.git .

# Start database
docker-compose up -d

# Install requirements
pip install -r ./requirements.txt

# Change environment to development 
export APP_ENVIRONMENT=dev

# Traditional Django commands
./src/manage.py makemigrations -y
./src/manage.py migrate -y
```

Then you can remove git history `rm -rf ./.git`

And start your own project. Enjoy it =)


### Working with initial data

The boilerplate contains some basic modifications to work with initial data. Django has already had the same mechanism
name "fixtures". But it works not very comfortable for real-world applications because need to append specific
prepared data.

Functionality of boilerplate enable you to create your own fixtures using Python code (I recommend you to look at
Faker and Factory Boy to make creating of Django entities more smoothly but you can do it using plain Python too).

Fixtures automatically apply after migrations in testing environment. In other environments you should execute console 
command `apply_migrations`.

## Contributing

You can be free to ask me questions and suggest new batteries or changes. 

**You are welcome with your pull requests** 

