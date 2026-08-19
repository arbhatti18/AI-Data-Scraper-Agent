import os
from crewai import Agent, LLM
from tools.scraper_tool import PlaywrightScraperTool
from tools.validator_tool import LeadStorageTool

def get_gemini_llm(api_key):
    os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6KmIiDdiQFiy4GK7IjKfGFK_x2o8PCLu9tkYwb9cAO4TQ"
    
    # Correct updated model string format for Gemini API
    return LLM(
        model="gemini/gemini-2.5-flash",
        api_key=api_key,
        temperature=0.1
    )

def create_scraper_agent(llm):
    return Agent(
        role="B2B Web Scraper",
        goal="Fetch raw webpage contents.",
        backstory="Expert web navigator.",
        tools=[PlaywrightScraperTool()],
        llm=llm
    )

def create_extractor_agent(llm):
    return Agent(
        role="Lead Extractor",
        goal="Extract structured leads from scraped text.",
        backstory="Senior B2B data analyst.",
        llm=llm
    )

def create_validator_agent(llm):
    return Agent(
        role="Lead Validator",
        goal="Validate and store clean lead data.",
        backstory="Data compliance manager.",
        tools=[LeadStorageTool()],
        llm=llm
    )