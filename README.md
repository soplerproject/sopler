Sopler
======

This is the source code of [sopler][sopler], a free / open source, social and collaborative web application that helps you make lists.
[sopler]: http://sopler.net/

Python packages
-------

On Fedora / CentOS:

`# yum install python-pip`

On Debian / Ubuntu:

`# apt-get install python-pip`

Run, Sopler!
-------
Follow these steps to download and run Sopler :

  `$ git clone git://github.com/soplerproject/sopler.git`
  
  `$ cd sopler`
  
  `$ pip install -r requirements.txt`
  
  ### Create your [SECRET_KEY][SECRET_KEY] in your ``settings.py`` file. ###
  [SECRET_KEY]: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
  `$ python manage.py syncdb`
  
  `$ python manage.py runserver`

You should then be able to open your browser on http://127.0.0.1:8000 and see Sopler's main page.

The css, js files and images will load properly, if you set the `DEBUG` parameter to `True` in your ``settings.py`` file or without any change to the `DEBUG` parameter just enter :

`$ python manage.py runserver --insecure`

License
-------
This software is licensed under the [GNU AFFERO GENERAL PUBLIC LICENSE][AGPL]. For more
information, read the file ``COPYING``.
