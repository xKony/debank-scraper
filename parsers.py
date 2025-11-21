from config import (
    MINIMUM_THRESHOLD_CHAIN,
    MINIMUM_THRESHOLD_PROJECT,
    MINIMUM_THRESHOLD_TOKEN,
)
import re


async def parse_chain_element(element_text: str) -> tuple[str | None, int | None]:
    element_text = element_text.strip()
    if "$" not in element_text:
        return None, None

    # nazwa chaina = wszystko przed $
    dollar_index = element_text.index("$")
    chain_name = element_text[:dollar_index].strip()

    # usd_value = token od $ do spacji po liczbie
    usd_value_str = element_text[dollar_index:].split()[0]  # np. "$6,004"

    # konwersja do liczby całkowitej
    try:
        usd_value_num = int(usd_value_str.replace("$", "").replace(",", ""))
    except ValueError:
        return None, None

    if usd_value_num < MINIMUM_THRESHOLD_CHAIN:
        return None, None

    return chain_name, usd_value_num


async def parse_project_element(line: str) -> tuple[str | None, int | None]:
    line = line.strip()
    if "$" not in line:
        return None, None

    # nazwa = wszystko przed $
    dollar_index = line.index("$")
    project_name = line[:dollar_index].strip()

    # usd_value = pierwszy token od $
    usd_value_str = line[dollar_index:].split()[0]  # np. "$1,324"

    try:
        usd_value_num = int(usd_value_str.replace("$", "").replace(",", ""))
    except ValueError:
        return None, None

    if usd_value_num < MINIMUM_THRESHOLD_PROJECT:
        return None, None

    return project_name, usd_value_num


async def parse_balance_with_percent(text: str) -> float:

    match = re.match(r"\s*\$([\d,.\s]+)", text)
    
    if not match:
        return 0.0

    usd = match.group(1)
    usd_clean = usd.replace(",", "").strip()
    usd_clean = usd_clean.replace(" ", "")

    try:
        return float(usd_clean)
    except ValueError:
        return 0.0


async def parse_token_element(
    line: str,
) -> tuple[str | None, float | None, float | None]:
    line = line.strip()
    if "$" not in line:
        return None, None, None

    # nazwa = wszystko przed $
    dollar_index = line.index("$")
    token_name = line[:dollar_index].strip()

    # usd_value = pierwszy token od $
    usd_value_str = line[dollar_index:].split()[0]  # np. "$1,324"
    try:
        usd_value_num = float(usd_value_str.replace("$", "").replace(",", ""))
    except ValueError:
        return None, None, None

    if usd_value_num < MINIMUM_THRESHOLD_PROJECT:
        return None, None, None

    # amount = jeśli w stringu jest separator "|" to bierz drugą część
    amount = 0.0
    if "|" in token_name:
        parts = token_name.split("|")
        token_name = parts[0].strip()
        if len(parts) >= 2:
            try:
                amount = float(parts[1].strip())
            except Exception:
                amount = 0.0

    return token_name, usd_value_num, amount
