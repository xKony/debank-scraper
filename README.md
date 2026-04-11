# 🏦 DeBank Portfolio Scraper

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Asyncio](https://img.shields.io/badge/Asyncio-Concurrency-green)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

<sub>this is my first Python project using an object-oriented structure - still learning</sub>

## 📋 Overview

This project is a high-performance, asynchronous tool designed to fetch crypto portfolio balances from DeBank.

Built using `nodriver` for robust browser automation, this tool is engineered to evade detection through fingerprint randomization, User-Agent rotation, and integrated NordVPN IP switching. It processes a list of wallet addresses and generates comprehensive reports in both CSV and XLSX _(MS Excel)_ formats, organizing data by Total Balance, Chains and Projects. Now includes **automated data visualization** to analyze your portfolio distribution at a glance.

_Partially **vibe-coded**, built for broke people like me that need to check balances for multiple addresses but don't have money to use Debank API._

## ✨ Key Features

- **Asynchronous Concurrency:** Uses `asyncio` with Semaphores to process multiple addresses simultaneously without overloading system resources.
- **Data Visualization:** Automatically generates professional-looking graphs (Boxplots, Histograms, Bar Charts) using `Seaborn` to visualize balance distribution across wallets, chains, and projects.
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
└── graphs/              # Automatically generated PNG plots
└── logs/                # Saved logs (optional)
├── addresses.txt        # Input file containing wallet addresses
├── browser_handler.py   # Handles DeBank class, parsing and navigation
├── graph_generator.py   # NEW: Visualization logic using Seaborn/Pandas
├── nodriver_utils.py    # Handles nodriver initialization
├── nordvpn_utils.py     # Handles NordVPN rotation
├── reporter.py          # Manages data aggregation, formatting, and file writing
├── config.py            # Central configuration file for thresholds and settings
├── main.py              # Entry point (orchestrator) with CLI flags
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

_(Ensure you have nodriver, pandas, seaborn, matplotlib, and openpyxl installed)._

## ⚙️ Configuration

All settings are managed in `config.py`. Below is a breakdown of new and critical options:

### Connection & Privacy

| Setting       | Type   | Description                                                                |
| ------------- | ------ | -------------------------------------------------------------------------- |
| `USE_NORDVPN` | `bool` | Enable/Disable NordVPN IP rotation.                                        |
| `BATCH_SIZE`  | `int`  | Number of addresses to process before rotating IP (e.g., randint(10, 20)). |
| `MAX_THREADS` | `int`  | Number of concurrent browser instances/tabs.                               |

### Visualization & Files

| Setting         | Type   | Description                                                              |
| --------------- | ------ | ------------------------------------------------------------------------ |
| `SAVE_GRAPHS`   | `bool` | Automatically generate and save PNG plots after each run.                |
| `GRAPHS_DIR`    | `str`  | Directory where plots are stored.                                        |
| `CSV_OUTPUT`    | `bool` | Generate `.csv` files.                                                   |
| `EXCEL_OUTPUT`  | `bool` | Generate `.xlsx` files (with multiple sheets).                           |
| `ADDRESSES_FILE`| `str`  | Path to the input list of addresses.                                     |

## 🚀 Usage

1. **Prepare Input:**
   Add the EVM wallet addresses you wish to check into `addresses.txt`, one per line.

2. **Run the Scraper:**
   ```Bash
   python main.py
   ```

3. **Run with Interactive Graphs:**
   To see the plots immediately after the scraping finishes:
   ```Bash
   python main.py --graphs
   ```

4. **Regenerate Graphs only:**
   If you already have data in `results/csv/` and just want to update the plots:
   ```Bash
   python graph_generator.py
   ```

## ⚠️ Disclaimer

This tool is developed for **educational purposes only**.

- The developer is not responsible for any misuse of this tool.
- Scraping data from websites may violate their Terms of Service.
- Use responsibly and ensure you adhere to the target website's robots.txt and policy guidelines.

## TO-DO

- proxy handling
- token parsing
- more advanced analytics (PnL tracking)

## 📜 License

**MIT**
