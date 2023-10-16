from selenium import webdriver  
from selenium.webdriver.common.by import By   
 
import time 
import getpass
from argparse import ArgumentParser


argument_parser = ArgumentParser()
argument_parser.add_argument("email", help="User email")
argument_parser.add_argument("url", help="Okta/login URL that redirects to Concur.")
argument_parser.add_argument("company", help="Company affiliation for all attendees.")
args = argument_parser.parse_args()
 
browser = webdriver.Firefox()
browser.implicitly_wait(20)

browser.get(args.url)
print(f"Logging in to {args.email} at {args.url}")
 
user = browser.find_element(By.ID, 'idp-discovery-username')

# Enter email
user.send_keys(args.email)
user.submit()
 
# Passcode, may be different depending on employer
passcode_input = browser.find_element(By.ID, 'input75')
passcode = getpass.getpass(f"Passcode for {args.email}: ")
passcode_input.send_keys(passcode)
passcode_input.submit()

reports_link = browser.find_element(By.PARTIAL_LINK_TEXT, "Open Reports")
reports_link.click()

# First report, may need to change
report_link = browser.find_element(By.CLASS_NAME, "sapcnqr-grid-list-item__link")
report_link.click()


time.sleep(4)
attendees = browser.find_element(By.CLASS_NAME, "attendees-link")
attendees.click()

attendees = browser.find_element(By.XPATH, "//span[@data-trans-id='attendees.viewAttendees']")
attendees.click()
time.sleep(3)


# Populate with your list of attendees
attendees = [
    ("FirstName1", "LastName1"),
    ("FirstName2", "LastName2")
]


add = browser.find_element(By.ID, 'attendees-add')
add.click()
time.sleep(3)

create = browser.find_element(By.CLASS_NAME, 'create-attendee__link')
create.click()
time.sleep(3)

for attendee in attendees:
    print(f"Adding {attendee}")
    last_name = browser.find_element(By.NAME, "lastName")
    last_name.send_keys(attendee[1])
    first_name = browser.find_element(By.NAME, "firstName")
    first_name.send_keys(attendee[0])
    company = browser.find_element(By.NAME, "company")
    company.send_keys(args.company)

    add_btn = browser.find_element(By.XPATH, "//span[@data-trans-id='attendees.createAttendee']")
    add_btn.click()

print("Done!")
