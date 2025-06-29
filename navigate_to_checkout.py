#!/usr/bin/env python3
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

    # Safe access to result properties
    if result is None:
        print("DEMONSTRATION FAILED - No result returned")
        return None

    # Check success status safely
    final_result = result.get('final_result', {})
    if final_result and final_result.get('success', False):
        print("DEMONSTRATION SUCCESSFUL")
    else:
        print("DEMONSTRATION COMPLETED (with simulation fallback)")
        if 'error' in result:
            print(f"Error encountered: {result['error']}")

    # Display achievements safely
    achievements = result.get('technical_achievements', [])
    if achievements:
        print("\nKey Achievements:")
        for achievement in achievements:
            print(f"  {achievement}")
    else:
        print("\nNo technical achievements recorded")

    # Display generated files safely
    try:
        print("\nFiles Generated:")
        log_filename = navigator.config.files.log_filename
        summary_filename = navigator.config.files.summary_filename
        print(f"  {log_filename}")
        print(f"  {summary_filename}")

        # Check for screenshots safely
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

    with open('session_results.json', 'w') as f:
        json.dump(result, f, indent=2, default=str)
