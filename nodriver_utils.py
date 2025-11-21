import nodriver as uc
import random
from fake_useragent import UserAgent
from config import USE_PROXY, HEADLESS_BROWSER

resolutions = [
    (1920, 1080),
    (1366, 768),
    (1536, 864),
    (1440, 900),
    (1600, 900),
    (1280, 720),
    (800, 600),
    (2560, 1440),
    (3840, 2160),
]


async def get_new_driver():
    w, h = (
        (random.choice(resolutions[0]) + random.randint(-20, 20)),
        (random.choice(resolutions[1]) + random.randint(-20, 20)),
    )
    user_agent = UserAgent().random
    lang = random.choice(["en-US", "en-GB", "fr-FR", "de-DE"])

    browser_args = [
        f"--window-size={w},{h}",
        f"--user-agent={user_agent}",
        random.choice(["--disable-gpu", "--enable-gpu"]),
        f"--force-device-scale-factor={random.uniform(1.0, 1.5)}",
        f"--renderer-process-limit={random.randint(5, 20)}",
        f"--screen-width={random.randint(1200, 2560)}",
        f"--screen-height={random.randint(800, 1440)}",
        "--disable-extensions",
        # randomize everything to ensure more unique fingerprints
    ]

    # proxy not working right now
    if USE_PROXY:
        browser_args.append(f"--proxy-server={USE_PROXY}")

    browser = await uc.start(
        browser_args=browser_args, headless=HEADLESS_BROWSER, lang=lang
    )

    return browser
