from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.common.exceptions import NoSuchElementException

import pandas as pd



# ALL_ LISTS
job_name, location, department, description, deadline = list(), list(), list(), list(), list()

###################
###  NTNU
###################
# Initialise webdriver
driver = webdriver.Firefox()

driver.get("https://www.ntnu.edu/vacancies")

# Initialise lists
# job_name, location, department, description, deadline = list(), list(), list(), list(), list()

# Push button to open all vacancies
driver.find_element_by_xpath("//button[@class='btn btn-outline-light btn-lg btn-block']").click()

# Find number of vacancies
num_of_elements = driver.find_elements_by_xpath('//div[3]/div/div/a').__len__()

# Read each entry
for i in range(num_of_elements):
    rel_xpath = '//div[3]/div/div/a[%r]' % (i+1)
    job_name.append(driver.find_element_by_xpath(rel_xpath + '/div[1]/h2').text)
    location.append(driver.find_element_by_xpath(rel_xpath + '/div[2]/div/div[1]').text)
    description.append(driver.find_element_by_xpath(rel_xpath + '/div[1]/p').text)
    department.append('None')
    deadline.append(driver.find_element_by_xpath(rel_xpath + '/div[2]/div/div[3]').text)

# Sort out non-phd offers
phds = ['phd', 'Phd', 'pHd', 'phD', 'PHd', 'PhD', 'PHD', 'pHD']
idx = [i for i, name in enumerate(job_name) if any(phd in name for phd in phds)]
job_name = [ele for i, ele in enumerate(job_name) if i in idx]
location = [ele for i, ele in enumerate(location) if i in idx]
description = [ele for i, ele in enumerate(description) if i in idx]
department = [ele for i, ele in enumerate(department) if i in idx]
deadline = [ele for i, ele in enumerate(deadline) if i in idx]

# Close browser
driver.quit()
del driver



###################
###  KTH
###################
driver = webdriver.Firefox()  # RECONNECT ERROR > Instantiate new driver instead

# Get kth website
driver.get("https://www.kth.se/en/om/work-at-kth/doktorander-1.572201")

# Initialise lists
# job_name, location, department, description, deadline = list(), list(), list(), list(), list()

# Read amount of table entries
all_tds = driver.find_elements_by_xpath('//tbody//tr//td')
assert len(all_tds) % 4 == 0, 'Number of elements is not a multiple of 4!'
num_of_elements = int(len(all_tds)/4)

# Read each entry
for i in range(num_of_elements):
    container = driver.find_elements_by_xpath('//tbody//tr[%r]//td' % (i+2))
    job_name.append(container[0].text)
    location.append(container[1].text)
    description.append('None')
    department.append(container[2].text)
    deadline.append(container[3].text)


# Close browser
driver.quit()
del driver



###################
###  PANDAS
###################
# Merge all_job_list into single list


# Read into pandas frame
df = pd.DataFrame({
    "name": job_name,
    "loc": location,
    "dep": department,
    "desc": description,
    "ddln": deadline
})

# Check readings
print(df.head)
print(df.loc[0])
print(df.loc[2])
print(df.info())





print('EOF')
