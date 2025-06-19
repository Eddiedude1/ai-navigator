#!/usr/bin/env python3
import argparse
import asyncio
from dotenv import load_dotenv
import os

from bunnings.navigator import AINavigator


async def main(config_file_path: str):
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(
            f"File path for config.toml is not correct, '{config_file_path}'"
        )

    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Please set ANTHROPIC_API_KEY environment variable")
        return

    navigator = AINavigator(
        config_path=config_file_path,
        anthropic_api_key=api_key
    )

    goal = navigator.config.general.goal

    print("Starting Interview Demonstration...")
    print(f"Goal: {goal}")

    result = await navigator.demonstrate_complete_solution(goal)

    # Final summary
    print("\n" + "="*80)
    print("INTERVIEW DEMONSTRATION COMPLETE")
    print("="*80)

    if result and result.get('final_result', {}).get('success'):
        print("DEMONSTRATION SUCCESSFUL")
    else:
        print("DEMONSTRATION COMPLETED (with simulation fallback)")

    if result:
        print("\nKey Achievements:")
        for achievement in result.get('technical_achievements', []):
            print(f"  {achievement}")

        print("\nFiles Generated:")
        log_filename = navigator.config.files.log_filename
        summary_filename = navigator.config.files.summary_filename
        print(f"  {log_filename}")
        print(f"  {summary_filename}")

        screenshots = result.get('final_result', {}).get('screenshots', [])
        for screenshot in screenshots:
            print(f"  {screenshot}")

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--configfile',
        default='config.toml',
        help='Filepath to the config file (default "config.toml")'
    )

    args = parser.parse_args()
    config_file_path = args.configfile

    asyncio.run(main(config_file_path=config_file_path))
