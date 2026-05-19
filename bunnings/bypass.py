"""
Cloudflare bypass strategies with adaptive human-behavior simulation.
"""

import asyncio
import random
import time
from typing import Dict, List, Tuple

from playwright.async_api import Page

from bunnings.ai_client import AIClient
from bunnings.config import Config


class BypassOrchestrator:
    """Runs multiple Cloudflare bypass strategies in sequence."""

    def __init__(self, config: Config, page: Page, ai_client: AIClient):
        self.config = config
        self.page = page
        self.ai_client = ai_client
        self._attempts: List[Dict] = []
        self._screenshots: List[str] = []

    @property
    def bypass_attempts(self) -> List[Dict]:
        return self._attempts

    @property
    def screenshots(self) -> List[str]:
        return self._screenshots

    async def demonstrate_strategies(self) -> Tuple[bool, List[Dict]]:
        """Run all configured bypass strategies in sequence.

        Returns:
            (success, attempts) — whether any strategy succeeded and the full attempt log.
        """
        strategy_names = self.config.bypass.strategies.names

        strategies = [
            (strategy_names[0] if len(strategy_names) > 0 else "Gradual Session Building",
             self._gradual_approach),
            (strategy_names[1] if len(strategy_names) > 1 else "Multi-Site Credibility",
             self._multi_site_approach),
            (strategy_names[2] if len(strategy_names) > 2 else "Direct with Patience",
             self._direct_approach)
        ]

        for strategy_name, strategy_func in strategies:
            print(f"\nAttempting: {strategy_name}")

            attempt_start = time.time()
            try:
                timeout_duration = self.config.bypass.strategies.timeout_per_strategy
                success = await asyncio.wait_for(
                    strategy_func(),
                    timeout=timeout_duration
                )

                attempt_duration = time.time() - attempt_start
                self._attempts.append({
                    'strategy': strategy_name,
                    'success': success,
                    'duration': attempt_duration
                })

                if success:
                    print(f"{strategy_name} succeeded in {attempt_duration:.1f}s!")
                    return True, self._attempts
                else:
                    print(f"{strategy_name} failed after {attempt_duration:.1f}s")

            except asyncio.TimeoutError:
                timeout_duration = self.config.bypass.strategies.timeout_per_strategy
                print(f"{strategy_name} timed out after {timeout_duration} seconds")
                self._attempts.append({
                    'strategy': strategy_name,
                    'success': False,
                    'duration': timeout_duration,
                    'reason': 'timeout'
                })
            except Exception as e:
                print(f"{strategy_name} error: {e}")

        print("\nAll bypass strategies exhausted")
        return False, self._attempts

    async def _gradual_approach(self) -> bool:
        """Build browser credibility gradually before navigating to target.

        1. Start from a neutral entry point
        2. Perform an unrelated search to establish browsing history
        3. Visit a credible Australian government site
        4. Search for hardware-related terms
        5. Locate target via search results
        6. Wait for Cloudflare resolution
        """
        print("   Building browsing session gradually...")
        session_cfg = self.config.session_building
        human_delay_cfg = self.config.human_behavior.delays
        elements_cfg = self.config.element_interaction
        general_cfg = self.config.general

        entry_point = random.choice(session_cfg.entry_points)
        print(f"   Step 1: Starting with {entry_point}...")
        await self.page.goto(entry_point, timeout=self.config.browser.default_timeout)
        await self._human_pause(
            human_delay_cfg.demo_behavior_min,
            human_delay_cfg.demo_behavior_max
        )

        print("   Step 2: Searching for weather (building credibility)...")
        unrelated_term = random.choice(session_cfg.search_terms.unrelated)
        await self._realistic_search(unrelated_term)
        await self._human_pause(
            human_delay_cfg.realistic_search_delay,
            human_delay_cfg.demo_behavior_max
        )

        print("   Step 3: Visiting Australian government site...")
        credible_site = random.choice(session_cfg.credibility_sites)
        await self.page.goto(credible_site, timeout=self.config.browser.default_timeout)
        await self._human_pause(
            human_delay_cfg.search_results_interaction_min,
            human_delay_cfg.search_results_interaction_max
        )

        print("   Step 4: Searching for hardware stores...")
        google_url = next(
            (url for url in session_cfg.entry_points if 'google' in url),
            session_cfg.entry_points[0]
        )
        await self.page.goto(google_url, timeout=self.config.browser.default_timeout)
        hardware_term = random.choice(session_cfg.search_terms.hardware_related)
        await self._realistic_search(hardware_term)
        await self._human_pause(
            human_delay_cfg.realistic_search_delay,
            human_delay_cfg.demo_behavior_max
        )

        print("   Step 5: Looking for Bunnings in search results...")
        try:
            bunnings_link = await self.page.wait_for_selector(
                elements_cfg.bunnings_link_selector,
                elements_cfg.bunnings_link_timeout
            )
            if bunnings_link:
                print("   Found Bunnings link, clicking...")
                await bunnings_link.click()
            else:
                print("   No link found, navigating directly...")
                await self.page.goto(
                    general_cfg.start_url,
                    timeout=self.config.browser.default_timeout
                )
        except Exception:
            print("   Direct navigation to Bunnings...")
            await self.page.goto(
                general_cfg.start_url,
                timeout=self.config.browser.default_timeout
            )

        print("   Step 6: Waiting for Cloudflare resolution...")
        return await self._cloudflare_wait(strategy_name="gradual")

    async def _multi_site_approach(self) -> bool:
        """Build credibility by visiting competitor sites before the target.

        1. Visit competitor hardware sites
        2. Simulate legitimate browsing behavior
        3. Approach target as part of comparison shopping
        4. Wait for Cloudflare resolution
        """
        print("   Building multi-site browsing pattern...")
        human_delays_cfg = self.config.human_behavior.delays
        competitor_sites = self.config.session_building.competitor_sites
        default_timeout = self.config.browser.default_timeout
        demo_min = human_delays_cfg.search_results_interaction_min
        demo_max = human_delays_cfg.demo_behavior_max

        for i, site in enumerate(competitor_sites, 1):
            try:
                print(f"   Step {i}: Visiting {site}...")
                await self.page.goto(site, timeout=default_timeout)
                await self._human_pause(demo_min, demo_max)
            except Exception as e:
                print(f"   Couldn't reach {site}: {e}")
                continue

        print(f"   Step {len(competitor_sites) + 1}: Approaching Bunnings...")
        await self.page.goto(self.config.general.start_url, timeout=default_timeout)
        return await self._cloudflare_wait(strategy_name="multisite")

    async def _direct_approach(self) -> bool:
        """Navigate directly to the target and wait patiently for resolution.

        1. Direct navigation to target
        2. Extended patience protocol with escalating interaction patterns
        """
        print("   Direct approach with extended patience...")
        await self.page.goto(
            self.config.general.start_url,
            timeout=self.config.browser.default_timeout
        )
        return await self._cloudflare_wait(strategy_name="direct")

    async def _cloudflare_wait(self, strategy_name: str = "unknown") -> bool:
        """Wait for Cloudflare to clear, taking periodic screenshots.

        Uses AI to detect whether the page is still a challenge or has resolved.
        Adapts mouse/scroll behavior based on elapsed wait time.
        """
        print("   Analyzing page for Cloudflare challenge...")

        max_wait = self.config.bypass.max_wait_time
        check_interval = self.config.bypass.check_interval
        total_waited = 0

        screenshot_freq = self.config.demo_mode.screenshot_frequency
        screenshot_prefix = self.config.files.screenshot_prefix
        screenshot_format = self.config.files.screenshot_format

        while total_waited < max_wait:
            if total_waited % screenshot_freq == 0:
                screenshot_path = (
                    f"{screenshot_prefix}_{strategy_name}_cloudflare_"
                    f"{total_waited}s.{screenshot_format}"
                )
                await self.page.screenshot(path=screenshot_path)
                self._screenshots.append(screenshot_path)

            is_resolved = await self._check_cloudflare_status()
            if is_resolved:
                print(f"   Cloudflare resolved after {total_waited}s!")
                return True

            patience_level = total_waited // 60
            patience_desc = [
                "minimal interaction",
                "reading simulation",
                "mild impatience",
                "moderate activity",
                "frustrated waiting"
            ]
            current_patience = min(patience_level, len(patience_desc) - 1)
            print(f"   {total_waited}s - Using {patience_desc[current_patience]}")

            await self._adaptive_behavior(patience_level)
            await asyncio.sleep(check_interval)
            total_waited += check_interval

        print(f"   Cloudflare not resolved within {max_wait}s")
        return False

    async def _check_cloudflare_status(self) -> bool:
        """Use AI to determine whether the page has cleared the Cloudflare challenge."""
        try:
            title = await self.page.title()
            content = await self.page.evaluate(
                "document.body.innerText.slice(0, "
                f"{self.config.ai.token_limits.page_analysis})"
            )

            analysis = await self.ai_client.analyze_page_status(
                url=self.page.url,
                title=title,
                content=content
            )

            if analysis.get('is_cloudflare_challenge', False):
                challenge_type = analysis.get('challenge_type', 'unknown')
                print(f"   Cloudflare {challenge_type} detected: '{title}'")
                return False

            if analysis.get('website_elements_present', False):
                print(f"   Website detected: '{title}'")
                return True

            print(f"   Status unclear: '{title}'")
            return False

        except Exception as e:
            print(f"   Check failed: {e}")
            return False

    async def _adaptive_behavior(self, patience_level: int):
        """Simulate human-like browser interaction scaled to elapsed wait time."""
        patience_cfg = self.config.cloudflare_detection.patience_levels

        if patience_level == 0:
            if random.random() < patience_cfg.level_0.mouse_movement:
                await self.page.mouse.move(
                    random.randint(400, 600),
                    random.randint(300, 500)
                )
        elif patience_level <= 2:
            if random.random() < patience_cfg.level_1.scroll_probability:
                scroll_amount = random.randint(-50, 100)
                await self.page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        else:
            action = random.choice(['scroll', 'move', 'key'])
            if action == 'scroll':
                await self.page.evaluate("window.scrollBy(0, 100)")
            elif action == 'move':
                await self.page.mouse.move(
                    random.randint(200, 800),
                    random.randint(200, 600)
                )
            elif action == 'key':
                await self.page.keyboard.press('Tab')

        thinking_pauses = self.config.human_behavior.timing.thinking_pauses
        await asyncio.sleep(random.uniform(thinking_pauses[0], thinking_pauses[1]))

    async def _human_pause(self, min_time: float, max_time: float):
        """Sleep for a random duration to simulate human reading/thinking time."""
        await asyncio.sleep(random.uniform(min_time, max_time))

    async def _realistic_search(self, query: str):
        """Type and submit a search query in the page's search box."""
        try:
            search_selectors = self.config.search_functionality.selectors
            for selector in search_selectors:
                try:
                    search_box = await self.page.wait_for_selector(
                        selector,
                        timeout=self.config.search_functionality.timeout
                    )
                    if search_box:
                        await search_box.click()
                        await asyncio.sleep(
                            self.config.search_functionality.submit_delay / 2000
                        )
                        await search_box.type(
                            query,
                            delay=self.config.search_functionality.typing_delay
                        )
                        await asyncio.sleep(
                            self.config.search_functionality.submit_delay / 1000
                        )
                        await search_box.press('Enter')
                        await asyncio.sleep(
                            self.config.search_functionality.results_wait / 1000
                        )
                        break
                except Exception:
                    continue
        except Exception:
            pass
