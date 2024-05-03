from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
import db


def calculate_days(date1, date2):
    date1 = datetime.strptime(date1, "%Y-%m-%d")
    date2 = datetime.strptime(date2, "%Y-%m-%d")

    delta = date2 - date1

    return abs(delta.days)

def scrape(driver, conn, dam):

    driver.get("https://www.cbr.washington.edu/dart/query/adult_daily")

    wait = WebDriverWait(driver, 100)

    actions = ActionChains(driver)

    start_month = "07"
    start_day = "01"

    end_month = "11"
    end_day = "1"

    year = "2023"

    start_date = year + "-" + start_month +"-" + start_day
    end_date = year + "-" + end_month + "-" + end_day

    #Locate form elements on web page after page has loaded
    form = driver.find_element(By.ID, "query")
    format_select = wait.until(EC.element_to_be_clickable((By.ID, "outputFormat1")))
    year_select = wait.until(EC.element_to_be_clickable((By.ID, "year-select")))
    dam_select = wait.until(EC.element_to_be_clickable((By.ID, "proj-select")))
    date_range_select = wait.until(EC.element_to_be_clickable((By.ID, "calendar")))
    date_start_select = wait.until(EC.element_to_be_clickable((By.ID, "startdate")))
    date_end_select = wait.until(EC.element_to_be_clickable((By.ID, "enddate")))
    run_select = wait.until(EC.element_to_be_clickable((By.ID, "run1")))
    submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Submit Query']")))

    #Clear pre-filled inputs and fill in form
    driver.execute_script("arguments[0].scrollIntoView(true);", form)

    select_year = Select(year_select)
    select_year.select_by_value(year)

    select_dam = Select(dam_select)
    select_dam.select_by_value(dam[0])

    actions.move_to_element(format_select)
    actions.click(format_select)
    actions.click()

    actions.move_to_element(date_range_select)
    actions.click(date_range_select)
    actions.perform()

    date_start_select.clear()
    date_start_select.send_keys(f"{start_month}/{start_day}")

    date_end_select.clear()
    date_end_select.send_keys(f"{end_month}/{end_day}")

    actions.move_to_element(run_select)
    actions.click(run_select)
    actions.perform()

    #Submit form
    actions.move_to_element(submit_btn)
    actions.click(submit_btn)
    actions.perform()

    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody")))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/dart/query/adult_daily"]')))

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, "html.parser")

    infobox = soup.find('tbody')

    salmon_counts = []
    dates = []
    dams = []

    # Check if infobox is found
    if infobox:
        infobox_fish_elements = infobox.find_all('td', class_='c0')
        infobox_date_elements = infobox.find_all('td', class_='rheader')

        for element in infobox_fish_elements:
            text = element.text.strip()
            if text:
                salmon_counts.append(int(element.text.strip()))
            else: salmon_counts.append(0)
        
        for element in infobox_date_elements:
            dams.append(dam[1])
            dates.append(element.text.strip())
    
    else: 
        days = calculate_days(start_date, end_date)
        date = datetime.strptime(start_date, "%Y-%m-%d")

        while days > 0:
            salmon_counts.append(0)
            dams.append(dam[1])
            dates.append(date.strftime("%Y-%m-%d"))
            date = date + timedelta(days=1)
            days -=1
    
    db.insert_data(conn, dates, salmon_counts, dams)
