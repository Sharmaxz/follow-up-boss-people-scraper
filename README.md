# Follow Up Boss People Scraper

A Python-based scraper/bot to extract contact information from the Follow Up Boss API. This tool fetches and processes contact data, storing it in a CSV file for easy access and analysis.

## Features

- Fetches contact data from the Follow Up Boss API.
- Processes and filters relevant contact fields.
- Handles primary email and phone identification.
- Outputs data to a CSV file.
- Includes error handling and logging for robust operation.

## Prerequisites

- Python 3.x
- `requests` library
- `python-dotenv` library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Sharmaxz/followupboss-people-scraper.git
    cd follow-up-boss-people-scraper
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your Follow Up Boss API key:
    ```
    FOLLOWUP_BOSS_API_KEY=your_api_key_here
    ```

## Usage

Run the scraper with:
```bash
python main.py
```

The script will fetch contacts from the Follow Up Boss API, process the data, and save it to contacts.csv.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.