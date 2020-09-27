from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.common.exceptions import NoSuchElementException
from emailing import send_peters_update


import pandas as pd


###################
###  Utility
###################
def build_df(data_list):
    df_all = pd.DataFrame()
    for d in data_list:
        df_tmp = pd.DataFrame({
            "deadline": d[0],
            "jobname": d[1],
            "location": d[2],
            "department": d[3],
            "description": d[4],
        })

        df_all = pd.concat([df_all, df_tmp])

    df_all.index = [i for i in range(len(df_all))]
    return df_all


def convert_to_html(dataframe):
    # Local safe
    dataframe.to_html("phd_jobs.html")
    dataframe.to_csv("phd_jobs.csv")

    # Compose table for email
    html_job_table = dataframe.to_html()

    return html_job_table


###################
###  Websites
###################
def get_ntnu():
    # Initialise lists
    job_name, location, department, description, deadline = list(), list(), list(), list(), list()

    # Initialise webdriver
    driver = webdriver.Firefox()
    driver.get("https://www.ntnu.edu/vacancies")

    # Push button to open all vacancies
    driver.find_element_by_xpath("//button[@class='btn btn-outline-light btn-lg btn-block']").click()

    # Find number of vacancies
    num_of_elements = driver.find_elements_by_xpath('//div[3]/div/div/a').__len__()

    # Read each entry
    for i in range(num_of_elements):
        rel_xpath = '//div[3]/div/div/a[%r]' % (i + 1)
        job_name.append(driver.find_element_by_xpath(rel_xpath + '/div[1]/h2').text)
        location.append(driver.find_element_by_xpath(rel_xpath + '/div[2]/div/div[1]').text)
        description.append(driver.find_element_by_xpath(rel_xpath + '/div[1]/p').text)
        department.append('None')
        deadline.append(driver.find_element_by_xpath(rel_xpath + '/div[2]/div/div[3]').text)

    # Sort out non-phd offers
    phds = ['phd', 'Phd', 'pHd', 'phD', 'PHd', 'PhD', 'PHD', 'pHD', 'Doctoral', 'doctoral']
    idx = [i for i, name in enumerate(job_name) if any(phd in name for phd in phds)]
    job_name = [ele for i, ele in enumerate(job_name) if i in idx]
    location = [ele for i, ele in enumerate(location) if i in idx]
    description = [ele for i, ele in enumerate(description) if i in idx]
    department = [ele for i, ele in enumerate(department) if i in idx]
    deadline = [ele for i, ele in enumerate(deadline) if i in idx]

    # Close browser
    driver.quit()
    del driver

    # Collect data
    return deadline, job_name, location, department, description


def get_kth():
    # Initialise lists
    job_name, location, department, description, deadline = list(), list(), list(), list(), list()

    # Get kth website
    driver = webdriver.Firefox()  # RECONNECT ERROR > Instantiate new driver instead
    driver.get("https://www.kth.se/en/om/work-at-kth/doktorander-1.572201")

    # Read amount of table entries
    all_tds = driver.find_elements_by_xpath('//tbody//tr//td')
    assert len(all_tds) % 4 == 0, 'Number of elements is not a multiple of 4!'
    num_of_elements = int(len(all_tds) / 4)

    # Read each entry
    for i in range(num_of_elements):
        container = driver.find_elements_by_xpath('//tbody//tr[%r]//td' % (i + 2))
        job_name.append(container[0].text)
        location.append(container[1].text)
        description.append('None')
        department.append(container[2].text)
        deadline.append(container[3].text)

    # Close browser
    driver.quit()
    del driver

    # Collect data
    return deadline, job_name, location, department, description


###################
###  Scrape the web
###################
data = [get_ntnu(), get_kth()]


# Read into pandas frame
df = build_df(data)


# Save data
html_table = convert_to_html(df)


# Send update
assert send_peters_update("Test", html_table), "Peter's update did not return with 1"



print('End of phd job collection')


#TODO Reformat dates to common format
#TODO Expand database
#TODO Automated update of job data base (manage a database)
#TODO Send regular/daily email to given email adress(es)
#TODO Run on py
