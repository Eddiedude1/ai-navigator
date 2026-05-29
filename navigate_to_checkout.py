#!/usr/bin/env python3
from dotenv import load_dotenv
import os

from src.navigator import Navigator


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

    navigator = Navigator(
        config_path=config_file_path,
        anthropic_api_key=api_key
    )

    goal = navigator.config.general.goal

    print("Starting navigation...")
    print(f"Goal: {goal}")

    result = await navigator.run(goal)

    print("\n" + "=" * 80)
    print("NAVIGATION COMPLETE")
    print("=" * 80)

    if result is None:
        print("NAVIGATION FAILED - No result returned")
        return None

    final_result = result.get('final_result', {})
    if final_result and final_result.get('success', False):
        print("NAVIGATION SUCCESSFUL")
    else:
        print("NAVIGATION COMPLETED (with simulation fallback)")
        if 'error' in result:
            print(f"Error encountered: {result['error']}")

    achievements = result.get('technical_achievements', [])
    if achievements:
        print("\nKey Achievements:")
        for achievement in achievements:
            print(f"  {achievement}")
    else:
        print("\nNo technical achievements recorded")

    try:
        print("\nFiles Generated:")
        log_filename = navigator.config.files.log_filename
        summary_filename = navigator.config.files.summary_filename
        print(f"  {log_filename}")
        print(f"  {summary_filename}")

        if final_result and 'screenshots' in final_result:
            screenshots = final_result.get('screenshots', [])
            for screenshot in screenshots:
                print(f"  {screenshot}")
        elif hasattr(navigator, 'screenshots') and navigator.screenshots:
            for screenshot in navigator.screenshots:
                print(f"  {screenshot}")
        else:
            print("  No screenshots captured")

    except Exception as e:
        print(f"Error accessing file information: {e}")

    return result


if __name__ == '__main__':
    import argparse
    import asyncio
    import json

    from src.config import load_config

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--configfile',
        default='config.toml',
        help='Filepath to the config file (default "config.toml")'
    )

    args = parser.parse_args()
    config_file_path = args.configfile

    result = asyncio.run(main(config_file_path=config_file_path))

    config = load_config(config_file_path)
    with open(config.files.results_filename, 'w') as f:
        json.dump(result, f, indent=2, default=str)
