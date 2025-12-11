# GenAI Projects Overview

## Two Agent Projects in Your Workspace

You now have **two complementary AI agent projects**:

### 1. 📚 Research & Task Automation Agent
**Location**: `/home/jairus/GenAI/research-agent/`

**Purpose**: General-purpose research and analysis agent

**Key Features**:
- ✅ ReAct (Reasoning + Acting) pattern
- ✅ Multiple LLM providers (OpenAI, Gemini)
- ✅ 6 built-in tools (web search, text analysis, file ops, code review, etc.)
- ✅ Batch processing
- ✅ Interactive CLI
- ✅ Production-ready architecture

**Use Cases**:
- Research automation
- Code analysis and review
- Content planning
- Project planning
- Technical documentation

**Tech Stack**:
- LangChain
- OpenAI GPT-4 / Google Gemini
- Python 3.10+

**Get Started**:
```bash
cd research-agent
pip install -r requirements.txt
export GEMINI_API_KEY="AIzaSyBBJ7TBSOiAadK0izwuH-zH4YOHQHopaF0"
python main.py "Your research question"
```

---

### 2. ⚡ Multi-Tool Weather & Time Agent
**Location**: `/home/jairus/GenAI/multi_tool_agent/`

**Purpose**: Specialized agent with specific tools (weather & time)

**Key Features**:
- ✅ Google ADK (Agent Development Kit)
- ✅ Multiple specialized tools
- ✅ Timezone handling
- ✅ Real-time weather data
- ✅ Lightweight and focused
- ✅ Easy to extend

**Use Cases**:
- Weather queries
- Time zone conversions
- Travel planning assistance
- Location-based information
- Extensible for custom tools

**Tech Stack**:
- Google ADK
- Gemini 2.0 Flash
- Python 3.10+

**Get Started**:
```bash
cd multi_tool_agent
pip install -r requirements.txt
python main.py "What's the weather in New York?"
```

---

## Comparison

| Feature | Research Agent | Multi-Tool Agent |
|---------|----------------|-----------------|
| **Framework** | LangChain | Google ADK |
| **LLM Support** | OpenAI, Gemini | Gemini |
| **Tool Count** | 6 general tools | 2 specific tools |
| **Complexity** | Advanced (ReAct) | Simple (direct tools) |
| **Setup Time** | ~5 minutes | ~2 minutes |
| **Extensibility** | Very high | High |
| **Use Case** | General research | Specific domains |
| **Cost** | Free (Gemini) | Free (Gemini) |

---

## Project Structures

### Research Agent
```
research-agent/
├── agent/
│   ├── core.py          # Multi-provider agent
│   ├── tools.py         # 6 general tools
│   ├── prompts.py       # System prompts
│   └── utils.py         # Utilities
├── examples/            # 4 example scripts
├── main.py              # CLI entry point
├── config.py            # Configuration
└── requirements.txt     # Dependencies
```

### Multi-Tool Agent
```
multi_tool_agent/
├── agent.py             # Agent with weather/time tools
├── main.py              # CLI entry point
├── .env                 # Configuration
├── requirements.txt     # Dependencies
└── README.md            # Documentation
```

---

## Which One Should You Use?

### Use Research Agent if you need:
- 🔍 Research and information gathering
- 📝 Content analysis and creation
- 💡 Problem solving and planning
- 🧠 Complex reasoning
- 🔄 Batch processing
- 🎯 Multiple LLM providers

### Use Multi-Tool Agent if you need:
- 🌤️ Specific domain tools
- ⚡ Quick responses
- 🛠️ Simple, focused functionality
- 🏗️ Easy-to-extend template
- 📱 Lightweight deployment
- 🎓 Learning ADK patterns

---

## Running Both Agents

### Terminal 1: Research Agent
```bash
cd /home/jairus/GenAI/research-agent
python main.py "Research the latest AI trends"
```

### Terminal 2: Multi-Tool Agent
```bash
cd /home/jairus/GenAI/multi_tool_agent
python main.py "What's the weather in Paris?"
```

---

## API Key Setup

Both agents use your Gemini API key:
```bash
export GEMINI_API_KEY="AIzaSyBBJ7TBSOiAadK0izwuH-zH4YOHQHopaF0"
```

Or create `.env` files in each project:
```
GEMINI_API_KEY=AIzaSyBBJ7TBSOiAadK0izwuH-zH4YOHQHopaF0
```

---

## Example Use Cases

### Research Agent Examples
```bash
# Research
python main.py "Research the impact of AI on healthcare"

# Analysis
python main.py "Analyze the top 5 programming languages for 2025"

# Planning
python main.py "Create a 6-month learning plan for machine learning"

# Code review
python main.py "Review this code: def add(a,b): return a+b"
```

### Multi-Tool Agent Examples
```bash
# Single query
python main.py "What's the weather in Tokyo?"

# Interactive mode
python main.py --interactive

# Test tools
python main.py --test-tools

# Combined
python main.py "What's the weather and time in London?"
```

---

## Extending Each Agent

### Adding Tools to Research Agent
Edit `agent/tools.py`:
```python
@tool
def my_new_tool(param: str) -> str:
    """Tool description."""
    return result

TOOLS.append(my_new_tool)
```

### Adding Tools to Multi-Tool Agent
Edit `agent.py`:
```python
def get_new_info(param: str) -> dict:
    """New tool implementation."""
    return {"status": "success", "report": "..."}

root_agent = Agent(
    ...
    tools=[get_weather, get_current_time, get_new_info],
)
```

---

## Recommended Learning Path

### Day 1: Multi-Tool Agent
1. Set up and run examples
2. Test the tools
3. Add a new tool (currency conversion)
4. Understand ADK patterns

### Day 2: Research Agent
1. Set up and run examples
2. Try different providers
3. Explore ReAct pattern
4. Add custom tools

### Day 3: Integration
1. Combine insights from both
2. Build a hybrid agent
3. Deploy to cloud
4. Optimize performance

---

## Next Steps

### Immediate
- ✅ Run both agents
- ✅ Test with your questions
- ✅ Explore examples

### Short-term
- 🔨 Add custom tools
- 📚 Read documentation
- 🧪 Experiment with prompts

### Long-term
- 🚀 Deploy to cloud
- 🔗 Integrate with web apps
- 📊 Monitor and optimize
- 🎯 Build production systems

---

## Troubleshooting

**Both agents failing?**
```bash
# Check API key
echo $GEMINI_API_KEY

# Set if needed
export GEMINI_API_KEY="AIzaSyBBJ7TBSOiAadK0izwuH-zH4YOHQHopaF0"
```

**Module not found?**
```bash
# Install dependencies
cd research-agent && pip install -r requirements.txt
cd ../multi_tool_agent && pip install -r requirements.txt
```

**Agent not responding?**
- Check internet connection
- Verify API key is correct
- Check API quotas at https://ai.google.dev/

---

## Resources

### Documentation
- [Research Agent README](research-agent/README_GEMINI.md)
- [Multi-Tool Agent README](multi_tool_agent/README.md)
- [Google ADK Docs](https://developers.google.com/agents)
- [Gemini API](https://ai.google.dev/)

### Learning
- [LangChain Docs](https://python.langchain.com/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Google AI Guide](https://ai.google.dev/)

### Support
- Check project READMEs for setup
- Review example scripts
- Check `.env` configuration

---

## Summary

| Aspect | Details |
|--------|---------|
| **Total Projects** | 2 (Research + Multi-Tool) |
| **Lines of Code** | 1000+ (across both) |
| **Tools Available** | 8 (6 + 2) |
| **LLM Providers** | OpenAI, Google Gemini |
| **Setup Time** | ~10 minutes |
| **Cost** | Free (using Gemini free tier) |
| **Ready for** | Production, Learning, Experimentation |

---

**You're all set! Both agents are ready to use.** 🚀

Choose the one that best fits your needs, or use both for different tasks!
