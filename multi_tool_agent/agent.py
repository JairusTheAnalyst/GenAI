"""Multi-Tool Agent with Weather and Time capabilities.

This agent demonstrates how to use Google's ADK to create an agent
with multiple tools that can answer questions about weather and time.
"""

import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    # Weather data for demonstration (can be replaced with real API)
    weather_data = {
        "new york": "sunny with a temperature of 25 degrees Celsius (77 degrees Fahrenheit)",
        "london": "cloudy with a temperature of 12 degrees Celsius (54 degrees Fahrenheit)",
        "tokyo": "rainy with a temperature of 18 degrees Celsius (64 degrees Fahrenheit)",
        "paris": "partly cloudy with a temperature of 15 degrees Celsius (59 degrees Fahrenheit)",
        "sydney": "clear skies with a temperature of 28 degrees Celsius (82 degrees Fahrenheit)",
    }
    
    city_lower = city.lower()
    if city_lower in weather_data:
        return {
            "status": "success",
            "report": f"The weather in {city} is {weather_data[city_lower]}.",
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """
    # Timezone mapping for demonstration
    timezone_map = {
        "new york": "America/New_York",
        "london": "Europe/London",
        "tokyo": "Asia/Tokyo",
        "paris": "Europe/Paris",
        "sydney": "Australia/Sydney",
    }
    
    city_lower = city.lower()
    if city_lower not in timezone_map:
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have timezone information for {city}.",
        }

    tz_identifier = timezone_map[city_lower]
    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    
    return {"status": "success", "report": report}


# Initialize the agent with tools
root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city. "
        "Use the available tools to get accurate information. Always be polite and helpful."
    ),
    tools=[get_weather, get_current_time],
)


def run_agent(user_query: str) -> str:
    """Run the agent with a user query.
    
    Args:
        user_query (str): The user's question or request.
        
    Returns:
        str: The agent's response.
    """
    try:
        response = root_agent.generate_content(user_query)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    # Example usage
    print("Weather & Time Agent")
    print("=" * 50)
    
    queries = [
        "What is the weather in New York?",
        "What time is it in Tokyo?",
        "Tell me about the weather and current time in Paris.",
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        response = run_agent(query)
        print(f"Response: {response}")
