# AI Navigator
An AI-First navigator for the site [bunnings.com](https://www.bunnings.com.au) the will find your item of interest and proceed to checkout.
- This POC uses Antrhopic API for AI decisioning
- Currenty built to run on a Unix OS
- Some packages are intentionally downgraded due to the old Mac OS virsion used to develope this project. 
- Python Versio: 3.9.23 (package/hardware restrained)
- Future Improvements: 
    - make application LLM agnostic for testing and fine tuning AI decision making
    - make application OS agnostic for a more seamless user experience
    - update application to use latest package and python versions to stay on the bleeding edge

**Outdated Macbook Specs:**  
```
Software:

    System Software Overview:

      System Version: macOS 10.14.6 (18G9323)
      Kernel Version: Darwin 18.7.0
      Boot Volume: Macintosh HD
      Boot Mode: Normal
      Computer Name: Guillermo_MBP
      User Name: Guillermo Gonzalez (guillermogonzalez)
      Secure Virtual Memory: Enabled
      System Integrity Protection: Enabled
      Time since boot: 14:05
```

## Environment Setup
1. Create a .env file  in the project's root dir with the contents below:
```
ANTHROPIC_API_KEY=...
```
2. Run: `$ ./setup.sh` (this will set up and activate your venv)

## Execution:
1. `$ ./navigate_to_checkout.py`


## Project Structure
```
.
├── README.md
├── .env ....................... NOT in version control
├── .gitignore
├── bunnings ................... Source Code
│   ├── config.py
│   └── navigator.py
├── config.toml ................. Application configuration
├── linting
│   ├── pep.sh .................. Flake8 pep8 report in stdout
│   ├── remove_whitespaces.sh ... Remove unwanted code whitespaces
│   └── todo.sh ................. Review all code todos
├── navigate_to_checkout.py ..... Navigator Execution Script
├── requirements.txt ............ Requirements.txt for easy environment replication
└── setup.sh .................... Optional virtual environment setup script 
```

## Navigator Execution Report
```
(py-tricentis) $ ./navigate_to_checkout.py 
Interview-Ready Navigator initialized
Demo mode: OFF
Starting Interview Demonstration...
Goal: Find a cordless drill and add it to the cart

================================================================================
INTERVIEW DEMONSTRATION: AI-DRIVEN WEB NAVIGATOR
================================================================================

PHASE 1: Configuration-Driven Architecture
--------------------------------------------------
Configuration loaded: AI Navigator 2025 v3.0.0
   - Browser strategies: 3
   - AI model: claude-3-5-sonnet-20241022
   - Max bypass attempts: 6
   - Adaptive timing: True
   - Fallback sites: 3

PHASE 2: Advanced Browser Setup with Stealth
--------------------------------------------------
Applying stealth configuration:
   - Removing automation artifacts
   - Spoofing browser fingerprints
   - Randomizing viewport and user agent
   - Injecting human behavior simulation
Advanced browser setup completed in 1.7s

PHASE 3: Intelligent Cloudflare Bypass
--------------------------------------------------

Attempting: Gradual Session Building
   Building browsing session gradually...
   Step 1: Starting with Google Australia...
   Step 2: Searching for weather (building credibility)...
   Step 3: Visiting Australian government site...
   Step 4: Searching for hardware stores...
   Step 5: Looking for Bunnings in search results...
   Direct navigation to Bunnings...
   Step 6: Waiting for Cloudflare resolution...
   Analyzing page for Cloudflare challenge...
2025-06-18 22:13:24 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   0s - Using minimal interaction
2025-06-18 22:13:43 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   15s - Using minimal interaction
2025-06-18 22:14:01 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   30s - Using minimal interaction
2025-06-18 22:14:19 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   45s - Using minimal interaction
2025-06-18 22:14:39 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   60s - Using reading simulation
2025-06-18 22:14:58 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   75s - Using reading simulation
2025-06-18 22:15:16 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   90s - Using reading simulation
2025-06-18 22:15:35 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   105s - Using reading simulation
2025-06-18 22:15:55 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   120s - Using mild impatience
2025-06-18 22:16:13 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   135s - Using mild impatience
Gradual Session Building timed out after 300 seconds

Attempting: Multi-Site Credibility
   Building multi-site browsing pattern...
   Step 1: Visiting https://www.mitre10.com.au...
   Step 2: Visiting https://www.supercheapauto.com.au...
   Step 3: Approaching Bunnings...
Multi-Site Credibility error: Navigation interrupted by another one
=========================== logs ===========================
navigating to "https://www.bunnings.com.au", waiting until "load"
============================================================
Note: use DEBUG=pw:api environment variable to capture Playwright logs.

Attempting: Direct with Patience
   Direct approach with extended patience...
   Analyzing page for Cloudflare challenge...
2025-06-18 22:17:04 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   0s - Using minimal interaction
2025-06-18 22:17:23 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   15s - Using minimal interaction
2025-06-18 22:17:42 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   30s - Using minimal interaction
2025-06-18 22:18:01 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   45s - Using minimal interaction
2025-06-18 22:18:19 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   60s - Using reading simulation
2025-06-18 22:18:37 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   75s - Using reading simulation
2025-06-18 22:18:58 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   90s - Using reading simulation
2025-06-18 22:19:18 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   105s - Using reading simulation
2025-06-18 22:19:37 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   120s - Using mild impatience
2025-06-18 22:19:57 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   135s - Using mild impatience
2025-06-18 22:20:18 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   150s - Using mild impatience
2025-06-18 22:20:36 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   165s - Using mild impatience
2025-06-18 22:20:56 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   180s - Using moderate activity
2025-06-18 22:21:16 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   195s - Using moderate activity
2025-06-18 22:21:37 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   210s - Using moderate activity
2025-06-18 22:21:58 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   Cloudflare browser_check detected: 'Just a moment...'
   225s - Using moderate activity
Direct with Patience timed out after 300 seconds

All bypass strategies exhausted

PHASE 4B: AI Navigation Simulation
--------------------------------------------------
Since Cloudflare bypass didn't succeed, demonstrating AI logic through simulation...

Simulation 1: Bunnings homepage with search box
2025-06-18 22:22:05 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   AI Decision: Type 'cordless drill' into the search box and press Enter/Submit - When looking for a specific product type like a cordless drill, using the search box is the most direct and efficient method rather than navigating through category menus. The search term 'cordless drill' is specific enough to return relevant results but not so narrow as to miss potential options. This is particularly effective on hardware store sites like Bunnings where product names are standardized.

Simulation 2: Search results for cordless drill
2025-06-18 22:22:12 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   AI Decision: Review and compare key drill specifications focusing on voltage, battery type, included batteries, torque levels, and user ratings - To find the best cordless drill match, we need to evaluate core features that indicate quality and value. Higher voltage (18V-20V) suggests more power, lithium-ion batteries offer better performance, inclusion of multiple batteries provides convenience, high torque ratings enable versatility, and positive user ratings validate real-world performance. Cross-referencing these factors helps identify the optimal choice.

Simulation 3: Specific drill product page
2025-06-18 22:22:17 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
   AI Decision: click on 'Add to Cart' button - Since we're already on a specific drill product page and the goal is to add the drill to the cart, the most direct action is to click the 'Add to Cart' button. This is typically prominently displayed on product pages and is the standard way to initiate a purchase. No need for additional product research or comparison since we've already selected the specific drill.

PHASE 5: Results Analysis and Technical Summary
--------------------------------------------------
Total session duration: 652.2s
Bypass attempts made: 2
AI decisions made: 29
Screenshots captured: 4

Technical Achievements:
   Externalized all configuration to TOML for easy modification
   Implemented comprehensive browser fingerprint evasion
   Demonstrated AI decision-making logic
   Showed context-aware navigation strategies
   Illustrated goal-oriented action planning

Configuration Management:
   All settings externalized to TOML
   No hardcoded values in application logic
   Easy modification for different sites/strategies

AI Navigation Capabilities:
   Natural language goal parsing
   Context-aware page analysis
   Intelligent action planning
   Adaptive strategy selection

Code Quality Features:
   PEP8 compliance with 90-character lines
   Comprehensive error handling
   Type hints throughout
   Detailed logging and monitoring

Session summary saved to interview_session_summary.json

================================================================================
INTERVIEW DEMONSTRATION COMPLETE
================================================================================
DEMONSTRATION SUCCESSFUL

Key Achievements:
  Externalized all configuration to TOML for easy modification
  Implemented comprehensive browser fingerprint evasion
  Demonstrated AI decision-making logic
  Showed context-aware navigation strategies
  Illustrated goal-oriented action planning

Files Generated:
  interview_session.log
  interview_session_summary.json
```

## Session Summary Json
```
{
  "total_time": 652.4752280712128,
  "bypass_attempts": [
    {
      "strategy": "Gradual Session Building",
      "success": false,
      "duration": 300,
      "reason": "timeout"
    },
    {
      "strategy": "Direct with Patience",
      "success": false,
      "duration": 300,
      "reason": "timeout"
    }
  ],
  "ai_decisions": 29,
  "screenshots": [
    "demo_cloudflare_0s.png",
    "demo_cloudflare_120s.png",
    "2_demo_cloudflare_0s.png",
    "2_demo_cloudflare_120s.png"
  ]
}
```

## Project Structure:
```
.
├── README.md
├── browser_profile.................Browswer profile created after first run
├── bunnings
│   ├── config.py
│   └── navigator.py
├── config.toml......................Application Configuration
├── navigate_to_checkout.py..........Execution Script
├── navigator_app.log................Logs
├── pep.sh...........................Pep8 Analysis
├── remove_whitespaces.sh............Remove unwanted whitespaces ./remove_whitespaces.sh bunnings/*.py
├── setup.sh.........................Virtual Environment Setup
├── tech_assignment_ai_research.pdf..Assignment Instructions
└── todo.sh..........................Review any code TODOs ./todo.sh
```

## config.toml user_agent configuration:
**Mac:**  
1. In terminal run `$ system_profiler SPSoftwareDataType SPHardwareDataType`
2. copy stdout
3. open an LLM chat
4. Use this prompt:
"""
I am using python playwright for some web automations and need help with creating a realistic user agent for my laptop with these specifications: 
```
<terminal-stdout>
```
I only need the user agent.
"""  
5. Copy the user agent into `config.toml` user_agent


SETUP:
> pip install undetected-playwright
> playwright install chromium
