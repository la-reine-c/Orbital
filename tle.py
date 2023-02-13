import orbit.tle
from lxml import html
import requests
import orbit as orb

def get(catnr):
    page = html.fromstring(requests.get('https://celestrak.org/NORAD/elements/gp.php?CATNR='+str(catnr)).text)
    tle = page.text.split('\n')
    return tle[0].strip(), tle[1].strip(), tle[2].strip()


orb.tle.get = get