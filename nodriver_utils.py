import nodriver as uc
from nodriver import cdp
import random
import os
import urllib.parse
from fake_useragent import UserAgent
from config import USE_PROXY, HEADLESS_BROWSER, PROXY_FILE

# Static list of resolutions
RESOLUTIONS = [
    (1920, 1080),
    (1366, 768),
    (1536, 864),
    (1440, 900),
    (1600, 900),
    (1280, 720),
    (2560, 1440),
    (3840, 2160),
]

# Initialize UserAgent once at module level to avoid blocking I/O on every call
ua = UserAgent()


def get_proxy():
    if not USE_PROXY:
        return None
    try:
        if os.path.exists(PROXY_FILE):
            with open(PROXY_FILE, "r") as f:
                proxies = [line.strip() for line in f if line.strip()]
            if proxies:
                return random.choice(proxies)
    except Exception as e:
        print(f"Error reading proxies from {PROXY_FILE}: {e}")
    return None


async def get_new_driver():
    # Pick a specific resolution tuple first to ensure realistic window sizes
    base_w, base_h = random.choice(RESOLUTIONS)
    w, h = base_w + random.randint(-20, 20), base_h + random.randint(-20, 20)

    user_agent = ua.random
    lang = random.choice(["en-US", "en-GB", "fr-FR", "de-DE"])

    browser_args = [
        f"--window-size={w},{h}",
        f"--user-agent={user_agent}",
        random.choice(["--disable-gpu", "--enable-gpu"]),
        f"--force-device-scale-factor={random.uniform(1.0, 1.5)}",
        f"--renderer-process-limit={random.randint(5, 20)}",
        "--disable-extensions",
        # randomize everything to ensure more unique fingerprints
    ]

    proxy = get_proxy()
    proxy_auth = None

    if proxy:
        if "://" in proxy:
            parsed = urllib.parse.urlparse(proxy)
            proxy_addr = f"{parsed.scheme}://{parsed.hostname}"
            if parsed.port:
                proxy_addr += f":{parsed.port}"
            if parsed.username and parsed.password:
                proxy_auth = (parsed.username, parsed.password)
        else:
            parts = proxy.split(":")
            if len(parts) == 4:  # ip:port:user:pass
                proxy_addr = f"http://{parts[0]}:{parts[1]}"
                proxy_auth = (parts[2], parts[3])
            elif len(parts) == 2:  # ip:port
                proxy_addr = f"http://{parts[0]}:{parts[1]}"
            else:
                proxy_addr = proxy  # fallback

        browser_args.append(f"--proxy-server={proxy_addr}")

    browser = await uc.start(
        browser_args=browser_args, headless=HEADLESS_BROWSER, lang=lang
    )

    if proxy_auth:
        tab = browser.main_tab
        # Enable request interception for authentication
        await tab.send(cdp.fetch.enable(handle_auth_requests=True))

        async def auth_handler(event: cdp.fetch.AuthRequired):
            await tab.send(
                cdp.fetch.continue_with_auth(
                    request_id=event.request_id,
                    auth_challenge_response=cdp.fetch.AuthChallengeResponse(
                        response="ProvideCredentials",
                        username=proxy_auth[0],
                        password=proxy_auth[1],
                    ),
                )
            )

        tab.add_handler(cdp.fetch.AuthRequired, auth_handler)

    return browser
