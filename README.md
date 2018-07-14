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


## Contribution

You can be free to ask me questions and suggest new batteries or changes. 

**You are welcome with your pull requests** 

