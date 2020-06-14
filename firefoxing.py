from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import pandas as pd


# Load website
driver = webdriver.Firefox()
driver.get("https://www.kth.se/en/om/work-at-kth/doktorander-1.572201")


# Initialise lists
job_name, location, department, deadline = list(), list(), list(), list()

# Read amount of table entries
all_tds = driver.find_elements_by_xpath('//tbody//tr//td')
assert len(all_tds) % 4 == 0, 'Number of elements is not a multiple of 4!'
num_of_container = int(len(all_tds)/4)

# Read each entry
for i in range(num_of_container):
    container = driver.find_elements_by_xpath('//tbody//tr[%r]//td' % (i+2))
    job_name.append(container[0].text)
    location.append(container[1].text)
    department.append(container[2].text)
    deadline.append(container[3].text)


# Close browser
driver.quit()


# Read into pandas frame
df_kth = pd.DataFrame({
    "name": job_name,
    "loc": location,
    "dep": department,
    "ddln": deadline
})

# Check readings
print(df_kth.head)
print(df_kth.loc[0])
print(df_kth.loc[2])
print(df_kth.info())





print('EOF')
