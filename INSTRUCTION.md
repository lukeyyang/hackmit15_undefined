# 

# initialization



>- Install `pip`
  + `sudo easy_install pip`
  + Or follow [instructions here](https://pip.pypa.io/en/latest/installing.html)
>- Install, create, and activate `virtualenv`
  + `sudo pip install virtualenv`
  + `virtualenv venv`
  + `. venv/bin/activate`
  + **note** If your python is Python 3.4, steps for installation and activation
of `virtualenv` may be different. The python I am using is Python 2.7.
>- Install requirements:
  + `pip install -r requirements.txt`
>- Install SQLite3
  If it does not exist already in your machine, please use your favorite package
manager (most likely you have one in your Linux) or [homebrew](brew.sh) (if you
are running OS X) to install `sqlite3`


## STOP HERE. ask lukeyyang for the Google API secret json file

>- Run the web app
 + `python run.py`
 + check out 127.0.0.1:5000 in your browser


>- Initialize the database 

 + `mkdir tmp`
 + `python db_create.py` 


>- Reset the database
 + `rm tmp/hh.py`


