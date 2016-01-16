# Heroku-Hello

Check the status of multiple Heroku projects to ensure they're online


### Usage

Simple! Add a list of Heroku sites to sites.log (separate them each by a newline), and run heroku-hello.py

```bash
$ pip install requests
$ chmod 775 sites.log
$ python heroku-hello.py
```

Too keep script running in the background, the crontab should look something like this (replace `~/Repos/` with the path to the script on your own system)

```
# Keep alive from 7am to 11pm (to obey Heroku free-tier limits)
*/60 7-23 * * * ~/Repos/heroku-hello/heroku-hello.py  
```


### Notes

* Python 2.7.10
* Tested on OS X and Linux


### TODO

* Add scheduler to keep Heroku VMs from going to sleep that doesn't depend on crontab

