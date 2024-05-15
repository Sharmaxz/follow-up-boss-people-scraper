import os
import requests
import csv
import time
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
URL = "https://api.followupboss.com/v1/people?limit=100&offset={}"
CSV_FILENAME = "people.csv"
INCLUDED_FIELDS = [
    "name", "firstName", "lastName", "email", "phone", "stage",
    "created", "updated", "lastActivity", "collaborators", "contacted",
    "tags", "emails", "phones"
]

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load API key from environment variable
API_KEY = os.getenv('FOLLOWUP_BOSS_API_KEY')
if not API_KEY:
    raise ValueError("API key not found. Please set the FOLLOWUP_BOSS_API_KEY environment variable.")

HEADERS = {'Authorization': f'Basic {API_KEY}'}


def fetch_contacts(page_number):
    """Fetch contacts from API for a specific page."""
    response = requests.get(URL.format(100 * page_number), headers=HEADERS)
    if response.status_code != 200:
        response.raise_for_status()
    return response.json()


def process_person(person):
    """Process a single contact and filter relevant fields."""
    person['email'] = ''
    person['phone'] = ''
    filtered_person = {field: person[field] for field in INCLUDED_FIELDS}

    for email in filtered_person["emails"]:
        if email['isPrimary'] == 1:
            filtered_person["email"] = email["value"]

    for phone in filtered_person["phones"]:
        if phone['isPrimary'] == 1:
            filtered_person["phone"] = phone["value"]

    filtered_person["collaborators"] = [collaborator["name"] for collaborator in filtered_person["collaborators"]]

    return filtered_person


def write_contacts_to_csv(contacts):
    """Write processed contacts to a CSV file."""
    with open(CSV_FILENAME, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=INCLUDED_FIELDS)
        writer.writeheader()
        for contact in contacts:
            writer.writerow(contact)


def main():
    """Main function to fetch, process, and save contacts."""
    page_number = 0
    contacts = []
    error_counter = 0
    start_time = time.time()

    while True:
        logging.info(f"Fetching page {page_number}...")
        try:
            data = fetch_contacts(page_number)
        except requests.HTTPError as e:
            error_counter += 1
            logging.error(f"Error fetching page {page_number}: {e}")
            if error_counter > 10:
                break
            time.sleep(5)
            continue

        metadata = data.get("_metadata", {})
        people = data.get("people", [])

        for person in people:
            contacts.append(process_person(person))

        if metadata.get("next") is None:
            break

        page_number += 1
        error_counter = 0

    write_contacts_to_csv(contacts)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f'Finished fetching {page_number} pages.')
    logging.info(f'Total time taken: {elapsed_time:.2f} seconds')


if __name__ == "__main__":
    main()