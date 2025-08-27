# LuxMedScrapper

A simple Python automation script that uses [Playwright](https://playwright.dev/python/) to log in to the **LuxMed Portal**, search for a specific medical service, and count available appointment slots.  

## Features

- Automatic login to LuxMed patient portal  
- Handling of post-login popups  
- Search for a specified medical service  
- Count available appointment slots  
- Outputs result as JSON  

## Requirements

- Python 3.9+  
- [Playwright for Python](https://playwright.dev/python/)  
- [loguru](https://github.com/Delgan/loguru) for logging  
- [python-dotenv](https://pypi.org/project/python-dotenv/) for environment variable management  

## Installation

1. Clone the repository or copy the script.  
2. Install dependencies:  

   ```bash
   pip install playwright loguru python-dotenv
   playwright install
