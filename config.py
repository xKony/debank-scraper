from random import randint

# CONFIGURATION FILE

### CONNECTION AND PRIVACY ###
USE_PROXY = False  # whether to use proxy connection (not working right now)
USE_NORDVPN = True  # whether to use nordvpn for IP rotation
BATCH_SIZE = randint(
    10, 20
)  # rotate nordvpn after X addresses (0 = no rotation) (if not using NORDVPN, this setting does nothing)
DEBANK_URL = "https://debank.com/profile/"

### PROCESSING ADDRESSES ###
CHAINS = True  # whether to process chains data
PROJECTS = True  # whether to process projects data
TOKENS = False  # whether to process tokens data (doesn't work right now)
MINIMUM_THRESHOLD_CHAIN = 1  # minimum USD value to consider (for a chain) (default 1 - to prevent saving 0$ chains)
MINIMUM_THRESHOLD_PROJECT = 0  # minimum USD value to consider (for a project)
MINIMUM_THRESHOLD_TOKEN = 1.0  # minimum USD value to consider (for a token)
MAX_PROJECTS = 0  # 0 means no limit (per account) if set returns X top projects
MAX_CHAINS = 0  # 0 means no limit (per account) if set returns X top chains
MAX_THREADS = 4  # number of concurrent threads for processing addresses
MAX_TOKENS = 0  # 0 means no limit (per account) if set returns X top tokens

### FILES ###
CSV_OUTPUT = True  # write result to csv file
EXCEL_OUTPUT = True  # write result to xlsx file (MS Excel)
ADDRESSES_FILE = "addresses.txt"  # file with list of addresses to process
PROXY_FILE = "proxies.txt"  # file with list of proxies to use (if USE_PROXY is True)

### OTHER SETTINGS ###
LOG_LEVEL = "INFO"  # logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
SAVE_LOGS = False  # whether to save browser logs to files
HEADLESS_BROWSER = True  # whether to run browser in headless mode
