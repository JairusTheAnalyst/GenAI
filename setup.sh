#!/bin/bash
# Quick Setup Script for GenAI Projects

set -e

echo "🚀 GenAI Projects Setup"
echo "========================"

# Set API Key
API_KEY="AIzaSyBBJ7TBSOiAadK0izwuH-zH4YOHQHopaF0"
export GEMINI_API_KEY="$API_KEY"
export GOOGLE_API_KEY="$API_KEY"

echo "✅ API Key configured"

# Setup Multi-Tool Agent
echo ""
echo "📦 Setting up Multi-Tool Agent..."
cd /home/jairus/GenAI/multi_tool_agent

if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✅ Virtual environment created"
fi

source venv/bin/activate
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

echo ""
echo "🌤️  Testing Multi-Tool Agent..."
python -c "
from multi_tool_agent.agent import get_weather, get_current_time
w = get_weather('New York')
t = get_current_time('New York')
print('Weather:', 'OK' if w['status'] == 'success' else 'FAIL')
print('Time:', 'OK' if t['status'] == 'success' else 'FAIL')
"

# Setup Research Agent
echo ""
echo "📦 Setting up Research Agent..."
cd /home/jairus/GenAI/research-agent

if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✅ Virtual environment created"
fi

source venv/bin/activate
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

echo ""
echo "════════════════════════════════════════"
echo "✅ ALL PROJECTS READY!"
echo "════════════════════════════════════════"

echo ""
echo "Quick Start Commands:"
echo ""
echo "1️⃣  Multi-Tool Agent (Weather & Time):"
echo "   cd /home/jairus/GenAI/multi_tool_agent"
echo "   python main.py \"What's the weather in Tokyo?\""
echo ""
echo "2️⃣  Research Agent:"
echo "   cd /home/jairus/GenAI/research-agent"
echo "   python main.py \"Research AI trends in 2025\""
echo ""
echo "3️⃣  View Projects:"
echo "   cat /home/jairus/GenAI/PROJECTS_OVERVIEW.md"
echo ""
