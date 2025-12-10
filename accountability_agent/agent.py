from google.adk.agents import Agent

def check_budget_transparency(county: str) -> dict:
    if county.lower() == "garissa":
        return {"status": "success", "report": "Garissa County's budget transparency index is 72%."}
    else:
        return {"status": "error", "error_message": f"No data for {county} County."}

root_agent = Agent(
    name="accountability_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions about county budget transparency and governance.",
    instruction="You are a helpful AI agent that supports leadership accountability discussions.",
    tools=[check_budget_transparency],
)
