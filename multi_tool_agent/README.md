# Multi-Tool Agent - Setup Guide

## Overview

This is a **Google ADK (Agent Development Kit)** agent that demonstrates:
- Multiple tool integration
- Weather information retrieval
- Time zone handling
- Gemini 2.0 Flash model usage

## Project Structure

```
multi_tool_agent/
├── __init__.py          # Package initialization
├── agent.py             # Main agent with tools
├── .env                 # Environment configuration
├── requirements.txt     # Dependencies
├── main.py              # CLI entry point
└── README.md            # Documentation
```

## Prerequisites

- Python 3.10+
- Google API Key (free from https://ai.google.dev/)

## Installation

### 1. Create Virtual Environment
```bash
cd multi_tool_agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Configuration

### Update .env File

Edit `.env` with your settings:

```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=AIzaSyBBJ7TBSOiAadK0izwuH-zH4YOHQHopaF0
AGENT_NAME=weather_time_agent
AGENT_MODEL=gemini-2.0-flash
```

## Usage

### Method 1: Command Line

```bash
# Run the agent with a query
python -m multi_tool_agent "What's the weather in New York?"

# Interactive mode
python main.py
```

### Method 2: Python API

```python
from multi_tool_agent.agent import run_agent

response = run_agent("What time is it in Tokyo?")
print(response)
```

### Method 3: Direct Import

```python
from multi_tool_agent.agent import get_weather, get_current_time

weather = get_weather("London")
time = get_current_time("Paris")

print(weather)
print(time)
```

## Available Tools

### get_weather(city: str) -> dict
Retrieves weather information for a city.

**Example:**
```python
result = get_weather("New York")
# Returns: {"status": "success", "report": "The weather in New York is..."}
```

**Supported Cities:**
- New York
- London
- Tokyo
- Paris
- Sydney

### get_current_time(city: str) -> dict
Returns the current time in a specified city.

**Example:**
```python
result = get_current_time("Tokyo")
# Returns: {"status": "success", "report": "The current time in Tokyo is..."}
```

**Supported Cities:**
- New York
- London
- Tokyo
- Paris
- Sydney

## Example Queries

```bash
# Weather queries
"What is the weather in New York?"
"Tell me the weather for London and Tokyo"
"Is it sunny in Sydney?"

# Time queries
"What time is it in Paris?"
"What's the current time in Tokyo?"
"Tell me the time in New York and London"

# Combined queries
"What's the weather and current time in Paris?"
"Is it raining in Tokyo right now? What time is it there?"
```

## Adding New Tools

To add new tools to the agent:

1. Define a function that returns a dict with `status` and `report`/`error_message`
2. Add it to the agent's `tools` list

**Example:**
```python
def get_currency_exchange(from_currency: str, to_currency: str) -> dict:
    """Get exchange rate between currencies."""
    # Implementation here
    return {"status": "success", "report": "..."}

root_agent = Agent(
    ...
    tools=[get_weather, get_current_time, get_currency_exchange],
)
```

## Adding New Cities

Edit the timezone and weather data dictionaries in `agent.py`:

```python
timezone_map = {
    "new york": "America/New_York",
    "london": "Europe/London",
    "your_city": "Your/Timezone",  # Add here
}

weather_data = {
    "new york": "sunny...",
    "your_city": "weather description",  # Add here
}
```

## Environment Variables

| Variable | Value | Required |
|----------|-------|----------|
| GOOGLE_GENAI_USE_VERTEXAI | FALSE/TRUE | Yes |
| GOOGLE_API_KEY | Your API key | Yes |
| AGENT_NAME | Agent name | No |
| AGENT_MODEL | gemini-2.0-flash | No |

## Troubleshooting

### "ModuleNotFoundError: No module named 'google.adk'"
```bash
pip install google-adk
```

### "API Key not found"
- Check `.env` file has GOOGLE_API_KEY set
- Or set environment variable: `export GOOGLE_API_KEY="..."`

### "City not found"
- Add the city to the timezone_map and weather_data dictionaries
- Use lowercase city names in queries

## Model Options

The agent supports Gemini models:
- `gemini-2.0-flash` (Default, fastest)
- `gemini-2.0-flash-live-001` (Real-time streaming)
- `gemini-1.5-pro` (More capable, slower)

Update `AGENT_MODEL` in `.env` to use a different model.

## Advanced Features

### Real-time Weather API Integration
Replace mock data with actual API:

```python
import requests

def get_weather(city: str) -> dict:
    response = requests.get(f"https://api.weather.api/city/{city}")
    # Parse and return response
```

### Database Integration
Store and retrieve historical data:

```python
import sqlite3

def save_query(query: str, response: str):
    conn = sqlite3.connect("queries.db")
    # Save to database
```

### Streaming Responses
Enable real-time streaming:

```python
model = "gemini-2.0-flash-live-001"
response = root_agent.generate_content_stream(user_query)
for chunk in response:
    print(chunk.text, end="")
```

## Performance Tips

1. **Cache Tool Results** - Avoid repeated API calls
2. **Use Appropriate Model** - `gemini-2.0-flash` for speed
3. **Batch Requests** - Process multiple queries efficiently
4. **Monitor Usage** - Track API usage within free tier limits

## Free Tier Limits

- **Requests per minute**: 600
- **Tokens per minute**: 2,000,000
- **Daily requests**: Unlimited

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure API key
3. **Run example**: `python main.py`
4. **Add more tools**: Extend `agent.py`
5. **Deploy**: Package for production

## Resources

- [Google ADK Documentation](https://developers.google.com/agents)
- [Gemini API Reference](https://ai.google.dev/)
- [Python Google AI Library](https://github.com/google/google-ai-python-sdk)

## Support

For issues or questions:
1. Check `.env` configuration
2. Verify API key is correct
3. Review error messages
4. Check Google ADK documentation

---

**Status**: Ready for development  
**Last Updated**: 2025-12-11  
**Google ADK Version**: Latest
