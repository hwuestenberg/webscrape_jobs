import pandas as pd
from urllib.request import urlopen as uopen
from bs4 import BeautifulSoup as bsoup
import requests

# nature_url = "https://www.nature.com/"
kth_url = "https://www.kth.se/en/om/work-at-kth/doktorander-1.572201"
#chalmers_url = "https://www.chalmers.se/en/about-chalmers/vacancies/Pages/default.aspx"

# Open url and grab data
uClient = uopen(kth_url)
html = uClient.read()
uClient.close()


# Html parsing
soup = bsoup(html, "html.parser")


# Extract small boxes
containers = soup.findAll("a", {"class": "standardLink"})  # Get container
desc = [container.get_text() for container in containers]
link = [container.get('href') for container in containers]





jobs = pd.DataFrame({
    "desc": desc,
    "link": link
})


print(jobs)



print('EOF')
