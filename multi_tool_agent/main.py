#!/usr/bin/env python
"""Main entry point for the Multi-Tool Agent.

Usage:
    python main.py "Your question here"
    python main.py                     # Interactive mode
"""

import sys
import os
from dotenv import load_dotenv
from multi_tool_agent.agent import run_agent, get_weather, get_current_time

# Load environment variables
load_dotenv()


def interactive_mode():
    """Run the agent in interactive mode."""
    print("\n" + "=" * 60)
    print("  MULTI-TOOL WEATHER & TIME AGENT")
    print("=" * 60)
    print("\nType 'quit' or 'exit' to stop\n")
    
    while True:
        try:
            user_query = input("🤖 You: ").strip()
            
            if not user_query:
                continue
            
            if user_query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            print("\n⏳ Processing...\n")
            response = run_agent(user_query)
            print(f"🎯 Agent: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")


def single_query_mode(query: str):
    """Run the agent with a single query."""
    print("\n" + "=" * 60)
    print("  MULTI-TOOL WEATHER & TIME AGENT")
    print("=" * 60)
    print(f"\nQuery: {query}\n")
    
    response = run_agent(query)
    print(f"Response:\n{response}\n")
    
    return 0


def test_tools():
    """Test individual tools."""
    print("\n" + "=" * 60)
    print("  TESTING TOOLS")
    print("=" * 60)
    
    # Test weather tool
    print("\n📍 Testing get_weather():")
    cities = ["New York", "London", "Tokyo"]
    for city in cities:
        result = get_weather(city)
        status = "✅" if result["status"] == "success" else "❌"
        print(f"{status} {city}: {result.get('report', result.get('error_message'))}")
    
    # Test time tool
    print("\n🕐 Testing get_current_time():")
    for city in cities:
        result = get_current_time(city)
        status = "✅" if result["status"] == "success" else "❌"
        print(f"{status} {city}: {result.get('report', result.get('error_message'))}")
    
    print()


def show_help():
    """Display help message."""
    print("""
Multi-Tool Weather & Time Agent

Usage:
    python main.py "Your question here"     # Single query
    python main.py --interactive            # Interactive mode
    python main.py --test-tools             # Test tools
    python main.py --help                   # Show this help

Examples:
    python main.py "What's the weather in New York?"
    python main.py "What time is it in Tokyo?"
    python main.py "Tell me the weather and time in Paris"

Interactive Mode:
    python main.py --interactive
    Then type your questions at the prompt

Features:
    ✓ Weather information for multiple cities
    ✓ Current time in different timezones
    ✓ Gemini 2.0 Flash model
    ✓ Multi-tool integration

Available Cities:
    - New York
    - London
    - Tokyo
    - Paris
    - Sydney

Environment:
    GOOGLE_API_KEY      - Your Google API key
    AGENT_MODEL         - Model to use (default: gemini-2.0-flash)

Get API Key: https://ai.google.dev/
""")


def main():
    """Main entry point."""
    
    # Check API key
    if not os.getenv('GOOGLE_API_KEY'):
        print("""
❌ Google API Key not found!

Please set your API key:
    export GOOGLE_API_KEY="AIzaSy..."

Or update the .env file with:
    GOOGLE_API_KEY=AIzaSy...

Get your free API key at: https://ai.google.dev/
""")
        return 1
    
    # Parse arguments
    if len(sys.argv) < 2:
        # Interactive mode by default
        interactive_mode()
        return 0
    
    if sys.argv[1] in ['--help', '-h', 'help']:
        show_help()
        return 0
    
    if sys.argv[1] in ['--interactive', '-i']:
        interactive_mode()
        return 0
    
    if sys.argv[1] in ['--test-tools', '-t']:
        test_tools()
        return 0
    
    # Single query mode
    query = ' '.join(sys.argv[1:])
    return single_query_mode(query)


if __name__ == "__main__":
    sys.exit(main())
