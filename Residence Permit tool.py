import schedule
import time
import undetected_chromedriver as uc
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


# Add your SMTP server details, email credentials, and sender/recipient information here
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'update.and.notify.me.now@gmail.com'
sender_password = 'kpdmqmnxnxmhkjcw'
recipient_email = 'update.and.notify.me.now@gmail.com'

def check_appointments():
    # Create a new instance of the Chrome driver
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = uc.Chrome(options=chrome_options)

    # Open the website
    driver.get('https://otv.verwalt-berlin.de/ams/TerminBuchen')

    # Wait for the button to be clickable
    wait = WebDriverWait(driver, 120)  # Increased timeout to 10 seconds

    termin_buchen_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Termin buchen')))
    termin_buchen_button.click()

    # Find the checkbox element
    time.sleep(3)  # Delay for 3 seconds
    checkbox = wait.until(EC.element_to_be_clickable((By.ID, 'xi-cb-1')))
    checkbox.click()

    # Scroll down to ensure the "Weiter" button is in view
    driver.execute_script("window.scrollBy(0, 300)")

    # Click the Weiter button using class and text content
    weiter_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ui-button-text') and text()='Weiter']")))
    weiter_button.click()

    # Wait for the loading overlay to disappear
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.loading')))
    time.sleep(10)

    # Find the select element
    select_element = wait.until(EC.presence_of_element_located((By.ID, "xi-sel-400")))

    # Scroll down to the select element to make it visible
    driver.execute_script("arguments[0].scrollIntoView(true);", select_element)

    # Click on the select element to open the dropdown
    select_element.click()

    # Scroll down the dropdown list until the desired option is found
    option_text = "Australien"
    option_found = False

    while not option_found:
        try:
            option_element = driver.find_element(By.XPATH, f"//option[text()='{option_text}']")
            option_found = True
        except NoSuchElementException:
            # Scroll down the dropdown list by sending the DOWN arrow key
            select_element.send_keys(Keys.ARROW_DOWN)

    # Select the option by clicking on it
    option_element.click()

    # Find the select element
    select_element = wait.until(EC.presence_of_element_located((By.ID, 'xi-sel-422')))

    # Scroll down to the select element to make it visible
    driver.execute_script("arguments[0].scrollIntoView(true);", select_element)

    # Click on the select element to open the dropdown
    select_element.click()

    # Scroll down the dropdown list until the desired option is found
    option_text = "eine Person"
    option_found = False

    while not option_found:
        try:
            option_element = driver.find_element(By.XPATH, f"//option[text()='{option_text}']")
            option_found = True
        except NoSuchElementException:
            # Scroll down the dropdown list by sending the DOWN arrow key
            select_element.send_keys(Keys.ARROW_DOWN)

    # Select the option by clicking on it
    option_element.click()

    # Find the select element
    select_element = wait.until(EC.presence_of_element_located((By.ID, 'xi-sel-427')))

    # Scroll down to the select element to make it visible
    driver.execute_script("arguments[0].scrollIntoView(true);", select_element)

    # Click on the select element to open the dropdown
    select_element.click()

    # Execute JavaScript to select the last option
    driver.execute_script("arguments[0].selectedIndex = arguments[0].options.length - 1;", select_element)

    # Trigger the change event to reflect the selection
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", select_element)

    # Find and click on an empty element (e.g., the body element)
    empty_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//body")))
    empty_element.click()

    # Find the button using class name and click on it
    Aufenthaltstitel_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[contains(text(),'Aufenthaltstitel - beantragen')]")))
    Aufenthaltstitel_button.click()

    # Click Studium und Ausbildung
    studium_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'Studium und Ausbildung')]")))
    studium_button.click()

    # Scroll down to find the next button
    driver.execute_script("window.scrollBy(0, 500)")

    # Click Aufenthaltserlaubnis zum Studium
    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="SERVICEWAHL_DE523-0-1-3-305244"]')))
    next_button.click()

    # Wait for the loading overlay to disappear
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.loading')))

    # Scroll down to find the next button
    driver.execute_script("window.scrollBy(0, 500)")

    # Click Buchen button
    buchen_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="applicationForm:managedForm:proceed"]/span')))
    buchen_button.click()

    # Wait for the loading overlay to disappear
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.loading')))

    # Check if the page contains an error message
    #error_message_element = driver.find_element(By.XPATH, '//*[@id="messagesBox"]/ul/li')
    # Find the error message element using class name
    error_message_element = driver.find_elements(By.CLASS_NAME, 'errorMessage')

    if error_message_element:
        print("No Appointments Available")



    else:
        print("Bookings available")

        # Create the email message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = 'APPOINTMENTS AVAILABLE'
        body = 'Appointments are available. https://otv.verwalt-berlin.de/ams/TerminBuchen'
        message.attach(MIMEText(body, 'plain'))

        # Capture a screenshot of the page
        screenshot_path = 'screenshot.png'
        driver.save_screenshot(screenshot_path)

        # Attach the screenshot to the email
        with open(screenshot_path, 'rb') as file:
            screenshot = MIMEImage(file.read())
            screenshot.add_header('Content-Disposition', 'attachment', filename='screenshot.png')
            message.attach(screenshot)

        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Start the TLS connection
            server.starttls()

            # Log in to the Gmail account
            server.login(sender_email, sender_password)

            # Send the email
            server.send_message(message)

        # Delete the screenshot file
        os.remove(screenshot_path)

    # Quit the browser
    driver.quit()


# Schedule the job to run every 2 minutes
schedule.every(1).minutes.do(check_appointments)

# Keep the script running indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)
