"""
Playwright browser lifecycle management with stealth anti-detection.
"""

import random
from typing import Dict, List, Tuple

from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from playwright_stealth import Stealth

from bunnings.config import Config


class BrowserManager:
    """Manages Playwright browser setup with comprehensive fingerprint evasion."""

    def __init__(self, config: Config):
        self.config = config

    async def setup_browser(self) -> Tuple[Browser, BrowserContext, Page]:
        """Launch stealth browser and return (browser, context, page)."""
        playwright = await async_playwright().start()

        stealth_args = self._get_comprehensive_stealth_args()
        user_agent = self._generate_realistic_user_agent()
        viewport = self._get_randomized_viewport()

        launch_options = {
            'headless': self.config.browser.headless,
            'slow_mo': random.randint(
                self.config.browser.slow_mo_min,
                self.config.browser.slow_mo_max
            ),
            'args': stealth_args
        }

        browser = await playwright.chromium.launch(**launch_options)
        browser_geo_cfg = self.config.browser.geolocation
        context_options = {
            'viewport': viewport,
            'user_agent': user_agent,
            'locale': 'en-AU',
            'timezone_id': 'Australia/Sydney',
            'geolocation': {
                'latitude': (
                    browser_geo_cfg.latitude_base
                    + random.uniform(-browser_geo_cfg.variance,
                                     browser_geo_cfg.variance)
                ),
                'longitude': (
                    browser_geo_cfg.longitude_base
                    + random.uniform(-browser_geo_cfg.variance,
                                     browser_geo_cfg.variance)
                )
            },
            'permissions': ['geolocation'],
            'ignore_https_errors': True,
            'extra_http_headers': self._get_realistic_headers()
        }

        context = await browser.new_context(**context_options)
        await self._inject_stealth_script(context)

        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        page.set_default_timeout(self.config.browser.default_timeout)

        return browser, context, page

    async def cleanup(self, browser: Browser, context: BrowserContext):
        """Close browser context and browser."""
        if context:
            await context.close()
        if browser:
            await browser.close()

    def _get_comprehensive_stealth_args(self) -> List[str]:
        args = []
        args.extend(self.config.browser.args.core_stealth)
        args.extend(self.config.browser.args.advanced_stealth)
        args.extend(self.config.browser.args.fingerprint_evasion)
        args.extend(self.config.browser.args.performance_optimization)
        return args

    def _generate_realistic_user_agent(self) -> str:
        chrome_version = random.choice(
            self.config.browser.user_agents.chrome_versions
        )
        os_string = random.choice(
            self.config.browser.user_agents.os_combinations
        )
        return self.config.browser.user_agents.template.format(
            os=os_string,
            version=chrome_version
        )

    def _get_randomized_viewport(self) -> Dict[str, int]:
        return {
            'width': random.randint(
                self.config.browser.viewport.width_min,
                self.config.browser.viewport.width_max
            ),
            'height': random.randint(
                self.config.browser.viewport.height_min,
                self.config.browser.viewport.height_max
            )
        }

    def _get_realistic_headers(self) -> Dict[str, str]:
        return {
            'Accept': self.config.browser.headers.accept,
            'Accept-Language': self.config.browser.headers.accept_language,
            'Accept-Encoding': self.config.browser.headers.accept_encoding,
            'Cache-Control': self.config.browser.headers.cache_control,
            'Upgrade-Insecure-Requests':
                self.config.browser.headers.upgrade_insecure_requests,
            'Sec-Fetch-Dest': self.config.browser.headers.sec_fetch_dest,
            'Sec-Fetch-Mode': self.config.browser.headers.sec_fetch_mode,
            'Sec-Fetch-Site': self.config.browser.headers.sec_fetch_site,
            'Sec-Fetch-User': self.config.browser.headers.sec_fetch_user
        }

    async def _inject_stealth_script(self, context: BrowserContext):
        stealth_script = """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});

        Object.defineProperty(navigator, 'plugins', {
            get: () => [
                {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer'},
                {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai'},
                {name: 'Native Client', filename: 'internal-nacl-plugin'}
            ]
        });

        window.chrome = {
            runtime: {onConnect: undefined, onMessage: undefined},
            webstore: {install: () => {}, onInstallStageChanged: undefined},
            csi: () => ({startE: Date.now(), onloadT: Date.now()}),
            app: {isInstalled: false}
        };

        ['cdc_adoQpoasnfa76pfcZLmcfl_Array',
         'cdc_adoQpoasnfa76pfcZLmcfl_Promise',
         'cdc_adoQpoasnfa76pfcZLmcfl_Symbol',
         '$chrome_asyncScriptInfo',
         '$cdc_asdjflasutopfhvcZLmcfl_'].forEach(prop => delete window[prop]);
        """
        await context.add_init_script(stealth_script)
