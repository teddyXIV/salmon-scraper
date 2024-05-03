from selenium import webdriver
import db
import scraper     

def main():
    conn = db.connect_db()

    driver = webdriver.Chrome()

    dams = [
        ["BON", 1], 
        ["TDA", 2], 
        ["JDA", 3], 
        ["MCN", 4], 
        ["PRD", 5], 
        ["WAN", 6], 
        ["RIS", 7], 
        ["RRH", 8], 
        ["WEL", 9]
        ]
    
    for dam in dams:
        scraper.scrape(driver, conn, dam)

    driver.quit()

if __name__ == "__main__":
    main()
