from config import (
    MINIMUM_THRESHOLD_CHAIN,
    MINIMUM_THRESHOLD_PROJECT,
    MINIMUM_THRESHOLD_TOKEN,
)
import re

# Pre-compiled regex and translation table for performance
BALANCE_PATTERN = re.compile(r"\s*\$([\d,.\s]+)")
CLEAN_USD_TRANS = str.maketrans("", "", "$,")


def parse_chain_element(element_text: str) -> tuple[str | None, int | None]:
    element_text = element_text.strip()
    if "$" not in element_text:
        return None, None

    # chain name = everything before $
    try:
        dollar_index = element_text.index("$")
        chain_name = element_text[:dollar_index].strip()

        # usd_value = token from $ to the space after the number
        usd_value_str = element_text[dollar_index:].split()[0]  # e.g., "$6,004"

        # conversion to integer using fast translate
        usd_value_num = int(usd_value_str.translate(CLEAN_USD_TRANS))
    except (ValueError, IndexError):
        return None, None

    if usd_value_num < MINIMUM_THRESHOLD_CHAIN:
        return None, None

    return chain_name, usd_value_num


def parse_project_element(line: str) -> tuple[str | None, int | None]:
    line = line.strip()
    if "$" not in line:
        return None, None

    try:
        # name = everything before $
        dollar_index = line.index("$")
        project_name = line[:dollar_index].strip()

        # usd_value = first token from $
        usd_value_str = line[dollar_index:].split()[0]  # e.g., "$1,324"

        # fast translation
        usd_value_num = int(usd_value_str.translate(CLEAN_USD_TRANS))
    except (ValueError, IndexError):
        return None, None

    if usd_value_num < MINIMUM_THRESHOLD_PROJECT:
        return None, None

    return project_name, usd_value_num


def parse_balance_with_percent(text: str) -> float:
    match = BALANCE_PATTERN.match(text)
    if not match:
        return 0.0

    # Fast cleanup using translate + strip + replace space
    usd_clean = match.group(1).translate(CLEAN_USD_TRANS).replace(" ", "")

    try:
        return float(usd_clean)
    except ValueError:
        return 0.0


def parse_token_element(
    line: str,
) -> tuple[str | None, float | None, float | None]:
    line = line.strip()
    if "$" not in line:
        return None, None, None

    try:
        # name = everything before $
        dollar_index = line.index("$")
        token_name = line[:dollar_index].strip()

        # usd_value = first token from $
        usd_value_str = line[dollar_index:].split()[0]  # e.g., "$1,324"
        usd_value_num = float(usd_value_str.translate(CLEAN_USD_TRANS))
    except (ValueError, IndexError):
        return None, None, None

    if usd_value_num < MINIMUM_THRESHOLD_TOKEN:
        return None, None, None

    # amount = if separator "|" is in the string, take the second part
    amount = 0.0
    if "|" in token_name:
        parts = token_name.split("|")
        token_name = parts[0].strip()
        if len(parts) >= 2:
            try:
                amount = float(parts[1].strip())
            except (ValueError, IndexError):
                amount = 0.0

    return token_name, usd_value_num, amount
