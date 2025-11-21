import shutil
import os
import nodriver_utils
from parsers import (
    parse_chain_element,
    parse_project_element,
    parse_token_element,
    parse_balance_with_percent,
)
from config import (
    DEBANK_URL,
    MAX_CHAINS,
    MAX_PROJECTS,
    MAX_TOKENS,
    CHAINS,
    PROJECTS,
    TOKENS,
)
from reporter import write_raw_row
from random import uniform
import asyncio


class DebankProfile:
    def __init__(self, address: str):
        self.address = address
        self.browser = None
        self.page = None
        self.working = False
        self.user_data_dir = None

    async def start_browser(self):
        print("Starting browser for", self.address)
        self.working = True
        try:
            # We wrap the creation in a try/except to catch the timeout cancellation immediately
            self.browser = await nodriver_utils.get_new_driver()
            self.page = await self.browser.get(f"{DEBANK_URL}{self.address}")
            if hasattr(self.browser, "config") and hasattr(
                self.browser.config, "user_data_dir"
            ):
                self.user_data_dir = self.browser.config.user_data_dir
            await self.page.find(
                "Data updated", best_match=True, timeout=20
            )  # when this element appears the page should be fully loaded
            await asyncio.sleep(uniform(0.5, 1.5))  # ensure full load
            # parse total balance and check for 0$ (if balance = 0, skip further parsing)
            balance = await self.page.select("div[class*='HeaderInfo_totalAssetInner']")
            print(balance.text_all)
            if balance.text_all:
                bal_value = await parse_balance_with_percent(balance.text_all)
                write_raw_row(self.address, "total", "Total Balance", bal_value)
                if bal_value == 0.0:
                    print(f"⚠️ Address {self.address} has 0$ balance, skipping.")
                    # set working to false to skip further parsing
                    self.working = False

        except asyncio.CancelledError:
            print(f"⚠️ Browser start cancelled for {self.address}")
            raise
        except Exception as e:
            print(f"⚠️ Error in start_browser: {e}")
            raise e

    async def close_browser(self):
        if self.browser:
            try:
                # 1. Stop the browser process
                self.browser.stop()

                # 2. Wait for Windows to release file locks (Critical!)
                await asyncio.sleep(1.5)
                print(f"Closed browser for {self.address}")
                # delete temp user data dir, nodriver only does this once the script exits so to prevent wasting space
                # script does it manually here after closing the browser
                if self.user_data_dir and os.path.exists(self.user_data_dir):
                    try:
                        shutil.rmtree(self.user_data_dir, ignore_errors=True)
                        print(f"🧹 Cleaned up temp profile: {self.user_data_dir}")
                    except Exception as e:
                        print(f"⚠️ Could not delete temp dir: {e}")

            except Exception as e:
                print(f"⚠️ Error closing browser: {e}")
            finally:
                self.browser = None
                self.working = False
                self.page = None
                self.user_data_dir = None

    # parsing methods
    async def parse_chains(self):
        if self.working and CHAINS:
            # element that contains all chains
            chain_elements = await self.page.select_all(
                "div[class*='AssetsOnChain_filterable']"
            )
            # if the address has more chains than shown, click "Unfold" button
            unfold_button = await self.page.find("Unfold", best_match=True, timeout=3)
            if unfold_button:
                await unfold_button.mouse_click(button="left")
                await asyncio.sleep(uniform(0.5, 1.0))
                # now re-select all chain elements
                chain_elements = await self.page.select_all(
                    "div[class*='AssetsOnChain_filterable']"
                )
            print(f"Found {len(chain_elements)} chains")
            # loop through chains and parse
            for chain_element in chain_elements:
                if (MAX_CHAINS > 0) and (
                    chain_elements.index(chain_element) >= MAX_CHAINS
                ):
                    break
                name, value = await parse_chain_element(chain_element.text_all)
                # write to report if valid
                if name and value:
                    write_raw_row(self.address, "Chain", name, value)

    async def parse_projects(self):
        if self.working and PROJECTS:
            # element that contains all projects
            project_elements = await self.page.select_all(
                "div[class*='ProjectCell_assetsItemName']"
            )
            # same as in chains, check for "show all" button
            show_all_button = await self.page.find(
                "Protocols with small deposits are not displayed",
                best_match=True,
                timeout=3,
            )
            if show_all_button:
                await show_all_button.mouse_click(button="left")
                await asyncio.sleep(uniform(0.5, 1.0))
                project_elements = await self.page.select_all(
                    "div[class*='ProjectCell_assetsItemName']"
                )
            print(f"Found {len(project_elements)} projects")
            # iterate through projects and parse if valid
            for portfolio_element in project_elements:
                if (MAX_PROJECTS > 0) and (
                    project_elements.index(portfolio_element) >= MAX_PROJECTS
                ):
                    break
                name, value = await parse_project_element(portfolio_element.text_all)
                if name and value:
                    write_raw_row(self.address, "Project", name, value)

    # token parsing (not working right now)
    """
    async def parse_tokens(self):
        token_elements = await self.page.select_all(
            "div[class^='db-table TokenWallet_table'] div[class*='db-table-row']"
        )
        print(f"Found {len(token_elements)} tokens")
        await asyncio.sleep(uniform(0.5, 1.0))
        token_elements = await self.page.select_all(
            "div[class^='db-table TokenWallet_table'] div[class*='db-table-row']"
        )
        print(f"Found {len(token_elements)} tokens")
        for token_element in token_elements:

            index = token_elements.index(token_element)
            if (MAX_TOKENS > 0) and (index >= MAX_TOKENS):
                break
            name, usd_value, amount = await parse_token_element(token_element.text_all)

            if name and usd_value and amount:
                write_raw_row(self.address, "Token", name, f"{usd_value}|{amount}")
    """
