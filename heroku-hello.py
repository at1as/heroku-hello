#!/usr/bin/env python
from   multiprocessing import Process
import requests


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0"
RED, YELLOW, GREEN = "\033[31m", "\033[33m", "\033[32m"
CLEAR = "\033[0m"

def warn(text):
  print RED + "Warning: " + CLEAR + text

def error(text):
  print RED + "Error: " + CLEAR + text


def get_site_list():
  # Retrieve list of heroku URLs from sites.log file
  f = open('sites.log')
  site_list = f.readlines()
  site_list = [site.strip() for site in site_list]

  if not site_list == sorted(site_list):
    warn("Recommended to enter sites into sites.log in alphabetical order")
  
  f.close
  return site_list


def get_site_status(site_url):
  # Free-tier Heroku Apps can take up to about 30 seconds to come online
  try:
    r = requests.get(site_url, headers={'User-Agent': USER_AGENT}, allow_redirects=True, timeout=30)
  except requests.exceptions.ReadTimeout as e:
    error("Connection for %s timed out during read" %(site_url))
  except requests.exceptions.ConnectTimeout as e:
    error("Connection for %s timed out during connect" %(site_url))
  except requests.exceptions.ConnectionError as e:
    error("Connection Error for %s : %s" %(site_url, e))
  except Exception as e:
    error("Unknown exception for %s" %(site_url))
  else:
    if r.status_code == 200:
      status = GREEN + str(r.status_code) + CLEAR
    else:
      status = RED + str(r.status_code) + CLEAR
    print("\nSite: \t%s \nStatus: %s" %(site_url, status))


if __name__ == "__main__":

  sites = get_site_list()

  subprocesses = []
  # Check each site in a separate process so that a site that takes 30s to respond doesn't block the others
  for site in sites:
    p = Process(target=get_site_status, args=(site,))
    subprocesses.append(p)
    p.start()

  # Wait for all processes to complete
  for subprocess in subprocesses:
    subprocess.join()

