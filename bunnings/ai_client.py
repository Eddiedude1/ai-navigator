"""
Anthropic Claude API wrapper for AI-driven navigation decisions.
"""

import json
import logging
from typing import Dict

import anthropic

from bunnings.config import Config


class AIClient:
    """High-level interface to Claude for navigation decision-making."""

    def __init__(
        self,
        config: Config,
        anthropic_client: anthropic.Anthropic,
        logger: logging.Logger
    ):
        self.config = config
        self.client = anthropic_client
        self.logger = logger

    async def analyze_page_status(self, url: str, title: str, content: str) -> Dict:
        """Determine whether the page is a Cloudflare challenge or real content.

        Returns dict with: is_cloudflare_challenge, challenge_type, confidence,
        indicators_found, website_elements_present, recommendation.
        """
        prompt = self.config.prompts.cloudflare_detection.template.format(
            url=url,
            title=title,
            content_sample=content
        )
        response = await self._query_ai(
            prompt=prompt,
            system_prompt=self.config.prompts.cloudflare_detection.system,
            task_type='cloudflare_detection'
        )
        return self._parse_json(response)

    async def parse_goal(self, goal: str) -> Dict:
        """Extract structured intent from a natural language navigation goal.

        Returns dict with: primary_goal, product_keywords, action_type, preferences.
        """
        prompt = self.config.prompts.goal_parsing.template.format(goal=goal)
        response = await self._query_ai(
            prompt=prompt,
            system_prompt=self.config.prompts.goal_parsing.system,
            task_type='intent_parsing'
        )
        return self._parse_json(response)

    async def analyze_page(self, title: str, content: str) -> Dict:
        """Identify current page type and key interactive elements.

        Returns dict with: page_type, key_elements, next_actions.
        """
        prompt = self.config.prompts.page_analysis.template.format(
            title=title,
            content_sample=content
        )
        response = await self._query_ai(
            prompt=prompt,
            system_prompt=self.config.prompts.page_analysis.system,
            task_type='page_analysis'
        )
        return self._parse_json(response)

    async def decide_action(self, intent: Dict, page_analysis: Dict) -> Dict:
        """Select the next navigation action given goal intent and page state.

        Returns dict with: action, target, reasoning, confidence.
        """
        prompt = self.config.prompts.action_decision.template.format(
            intent=json.dumps(intent),
            page_analysis=json.dumps(page_analysis)
        )
        response = await self._query_ai(
            prompt=prompt,
            system_prompt=self.config.prompts.action_decision.system,
            task_type='decision_making'
        )
        return self._parse_json(response)

    async def simulate_scenario(self, scenario: Dict, goal: str) -> Dict:
        """Produce an AI decision for a hypothetical page scenario.

        Returns dict with: action, reasoning, expected_outcome.
        """
        prompt = self.config.prompts.simulation_decision.template.format(
            description=scenario['description'],
            goal=goal,
            ai_task=scenario['ai_task']
        )
        response = await self._query_ai(
            prompt=prompt,
            system_prompt=self.config.prompts.simulation_decision.system,
            task_type='decision_making'
        )
        return self._parse_json(response)

    def _parse_json(self, response: str) -> Dict:
        """Parse a JSON string returned by the AI, handling markdown code blocks."""
        stripped = response.strip()
        if stripped.startswith('```'):
            lines = stripped.split('\n')
            end = next(
                (i for i in range(len(lines) - 1, 0, -1) if lines[i].strip() == '```'),
                len(lines)
            )
            stripped = '\n'.join(lines[1:end]).strip()
        try:
            return json.loads(stripped)
        except json.JSONDecodeError as e:
            self.logger.warning(f"Non-JSON AI response ({e}): {response[:200]}")
            return {"error": "parse_failed"}

    async def _query_ai(
        self,
        prompt: str,
        system_prompt: str = "",
        task_type: str = "general"
    ) -> str:
        """Send a prompt to Claude and return the raw text response."""
        try:
            max_tokens = getattr(
                self.config.ai.token_limits,
                task_type,
                self.config.ai.max_tokens_default
            )

            api_params = {
                "model": self.config.ai.model,
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}]
            }

            if system_prompt:
                api_params["system"] = system_prompt

            response = self.client.messages.create(**api_params)
            return response.content[0].text

        except Exception as e:
            self.logger.error(f"AI query failed: {e}")
            return '{"error": "AI query failed"}'
