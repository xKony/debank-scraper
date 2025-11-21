# 🏦 DeBank Portfolio Scraper

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Asyncio](https://img.shields.io/badge/Asyncio-Concurrency-green)
![Status](https://img.shields.io/badge/Status-Active-success)

<sub>this is my first Python project using an object-oriented structure - still learning</sub>

## 📋 Overview

This project is a high-performance, asynchronous tool designed to fetch crypto portfolio balances from DeBank.

Built using `nodriver` for robust browser automation, this tool is engineered to evade detection through fingerprint randomization, User-Agent rotation, and integrated NordVPN IP switching. It processes a list of wallet addresses and generates comprehensive reports in both CSV and XLSX _(MS Excel)_ formats, organizing data by Total Balance, Chains and Projects.

_Partially **vibe-coded**, built for broke people like me that need to check balances for multiple addresses but don't have money to use Debank API._

## ✨ Key Features

- **Asynchronous Concurrency:** Uses `asyncio` with Semaphores to process multiple addresses simultaneously without overloading system resources.
- **Anti-Detection:**
  - Utilizes **nodriver** as the browser base.
  - Rotates User-Agents via `fake_useragent`.
  - Randomizes browser arguments to create unique browser fingerprints.
- **Privacy & IP Rotation:** Integrated `nordvpn-switcher-pro` to rotate IP addresses automatically after a configurable batch of addresses (e.g., every 10 wallets).
- **Smart Reporting:**
  - Outputs to CSV and XLSX.
  - Data sorted alphabetically while preserving the original input order of addresses.
  - Configurable thresholds (ignore chains/projects under specific $ amounts).
- **Robust Error Handling:** Logs browser activities and manages timeouts effectively.

## 📂 Project Structure

```text
└── results/             # Generated CSV/XLSX files
└── logs/                # Saved logs (optional)
├── addresses.txt        # Input file containing wallet addresses
├── proxies.txt          # Input file for proxies (optional, not working anyway)
├── browser_handler.py   # Handles DeBank class, parsing and navigation
├── nodriver_utils.py    # Handles nodriver initialization
├── nordvpn_utils.py     # Handles NordVPN rotation
├── reporter.py          # Manages data aggregation, formatting, and file writing
├── config.py            # Central configuration file for thresholds and settings
├── main.py              # Entry point (orchestrator)
├── parsers.py           # Handles parsing balances to correct format
├── logger.py            # Logs things
```

## ⚙️ Installation

1. **Clone the repository**:

```Bash
git clone https://github.com/xKony/debank-scraper.git
cd debank-scraper
```

2. **Install dependencies**:

```Bash
pip install -r requirements.txt
```

_(Ensure you have nodriver, fake_useragent, nordvpn-switcher-pro and openpyxl installed)._

## ⚙️ Configuration

All settings are managed in config.py. Below is a breakdown of available options:

### Connection & Privacy

| Setting       | Type   | Description                                                                |
| ------------- | ------ | -------------------------------------------------------------------------- |
| `USE_PROXY`   | `bool` | Enable/Disable proxy usage.                                                |
| `USE_NORDVPN` | `bool` | Enable/Disable NordVPN IP rotation.                                        |
| `BATCH_SIZE`  | `int`  | Number of addresses to process before rotating IP (e.g., randint(10, 20)). |
| `DEBANK_URL`  | `str`  | Base URL for the profile pages.                                            |

### Data Processing

| Setting                     | Type    | Description                                         |
| --------------------------- | ------- | --------------------------------------------------- |
| `CHAINS`                    | `bool`  | Scrape chain-specific data.                         |
| `PROJECTS`                  | `bool`  | Scrape DeFi project positions.                      |
| `TOKENS`                    | `bool`  | Scrape individual tokens (Currently not working).   |
| `MINIMUM_THRESHOLD_CHAIN`   | `float` | Minimum USD value to include a chain in the report. |
| `MINIMUM_THRESHOLD_PROJECT` | `float` | Minimum USD value to include a project position.    |
| `MAX_THREADS`               | `int`   | Number of concurrent browser instances/tabs.        |

### Data Processing

| Setting            | Type   | Description                                                        |
| ------------------ | ------ | ------------------------------------------------------------------ |
| `CSV_OUTPUT`       | `bool` | Generate `.csv` files.                                             |
| `EXCEL_OUTPUT`     | `bool` | Generate `.xlsx` files (with multiple sheets).                     |
| `ADDRESSES_FILE`   | `str`  | Path to the input list of addresses.                               |
| `HEADLESS_BROWSER` | `bool` | Run browser in background (True) or visible (False). `(debugging)` |

<sub>_more in `config.py`_</sub>

## 🚀 Usage

1.**Prepare Input:**

Add the EVM wallet addresses you wish to check into addresses.txt, one per line.

2.**Run the Script:**

```Bash
python main.py
```

3.**View Results:**

Check the results folder for the generated Excel or CSV files.

## ⚠️ Disclaimer

This tool is developed for **educational purposes only**.

- The developer is not responsible for any misuse of this tool.
- Scraping data from websites may violate their Terms of Service.
- Use responsibly and ensure you adhere to the target website's robots.txt and policy guidelines.

## TO-DO

- proxy handling
- token parsing

## 📜 License

**MIT**
