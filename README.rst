First Install Steps:
=====================

Requirements
-------------------

* Python 2.7
* Python headers (sudo apt-get install python-dev)
* CouchDB (sudo apt-get install couchdb)
* PostgreSQL (sudo apt-get install postgres)
* Geometry Engine - Open Source (sudo apt-get install geos)
* PostGIS (sudo apt-get install postgis)
* Pip (easy_install pip)
* VirtualEnv (pip install virtualenv)
* [Optional] VirtualEnvWrapper (pip install virtualenvwrapper)
* NumPy (pip install numpy)
* Geospatial Data Abstraction Library (sudo apt-get install gdal)

1. Create a virtualenv
--------------------
virtualenv ve && source ve/bin/activate
    or with virtualenvwrapper
mkvirtualenv mangrove

2. Install required python packages
--------------------
pip install -r requirements.pip

3. Create local_settings.py
--------------------
cp src/datawinners/local_settings_example.py src/datawinners/local_settings.py

4. Create Postgres DB
--------------------
createdb geodjango
createlang plpgsql geodjango
psql -d geodjango -c 'create role jenkins login createdb createrole;'
psql -d geodjango -f '/usr/local/Cellar/postgis/1.5.3/share/postgis/postgis.sql'
psql -d geodjango -f '/usr/local/Cellar/postgis/1.5.3/share/postgis/spatial_ref_sys.sql'
psql -d geodjango -c 'grant all privileges on all tables in schema public to jenkins;'

5. Load Shape Files
--------------------
Clone https://github.com/mangroveorg/shape_files.git as a sibling to mangrove
python src/datawinners/manage.py syncdb
python src/datawinners/manage.py migrate
python src/datawinners/manage.py loadshapes

Run tests!
=====================
./runtests.sh

Push to GitHub
=====================
And hopefully hudson will run tests, and they will pass.
