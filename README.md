Sopler
======

This is the source code of [sopler][sopler], a free / open source, social and collaborative web application that helps you make todo-lists.
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

  `$ su -c "pip install -r requirements.txt"`

  ### Create your [SECRET_KEY][SECRET_KEY] in your ``settings.py`` file. ###
  [SECRET_KEY]: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
  `$ python manage.py syncdb --all`

  `$ python manage.py runserver`

You should then be able to open your browser on http://127.0.0.1:8000 and see Sopler's main page.

The css, js files and images will load properly, if you set the `DEBUG` parameter to `True` in your ``settings.py`` file or without any change to the `DEBUG` parameter just enter :

`$ python manage.py runserver --insecure`

Data Migration - South
-------

Uncomment [south][south] (``settings.py`` file).
[south]: http://south.readthedocs.org/en/latest/

Initialization :

`$ python manage.py schemamigration core --initial`

`$ python manage.py syncdb` (optional - If complaining that `south_migrationhistory` does not exist)

`$ python manage.py migrate core` (in case of error, add the `--fake` parameter)


Change the model :

Add new field in your model (``models.py`` file).


Migration :

`$ python manage.py schemamigration core --auto`

`$ python manage.py migrate core`

License
-------
This software is licensed under the [GNU AFFERO GENERAL PUBLIC LICENSE][AGPL]. For more
information, read the file ``COPYING``.
