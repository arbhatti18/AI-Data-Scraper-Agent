import os, sqlite3, time
import pandas as pd
import streamlit as st
from crewai import Crew, Process
from agents import get_gemini_llm, create_scraper_agent, create_extractor_agent, create_validator_agent
from tasks import create_scraping_task, create_extraction_task, create_validation_task

st.title("🎯 AI Lead Generator (Gemini Powered)")

# User Inputs
api_key = st.text_input("Enter Google Gemini API Key", type="password", placeholder="AIzaSy...")
target_url = st.text_input("Target Web Directory URL", placeholder="https://example.com/directory")
target_icp = st.text_input("ICP Persona", value="CTO, Founders, Sales Heads")

# Start Lead Extraction
if st.button("Start Extraction"):
    if api_key and target_url:
        # Dynamic API key setting (No hardcoding)
        os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6KmIiDdiQFiy4GK7IjKfGFK_x2o8PCLu9tkYwb9cAO4TQ"
        
        try:
            # Initialize Gemini LLM Model
            llm = get_gemini_llm(api_key)
            
            # Create Agents
            scraper = create_scraper_agent(llm)
            extractor = create_extractor_agent(llm)
            validator = create_validator_agent(llm)
            
            # Setup CrewAI Sequential Workflow
            crew = Crew(
                agents=[scraper, extractor, validator],
                tasks=[
                    create_scraping_task(scraper, target_url),
                    create_extraction_task(extractor, target_icp),
                    create_validation_task(validator)
                ],
                process=Process.sequential
            )
            
            with st.spinner("Gemini Agents are scraping and processing leads..."):
                result = crew.kickoff()
                st.write(result.raw)
                st.success("Extraction Completed!")
                
        except Exception as e:
            st.error(f"Execution Error: {str(e)}")
            st.info("Tip: Agar '429 Rate Limit' error aaye to 1-2 minute ruk kar retry karein ya Google AI Studio se new project key generate karein.")
    else:
        st.warning("Please enter both API Key and Target URL.")

# View Extracted Data
if st.button("View Saved Leads"):
    try:
        conn = sqlite3.connect("leads_database.db")
        df = pd.read_sql_query("SELECT * FROM b2b_leads", conn)
        conn.close()
        
        if df.empty:
            st.warning("Database exists but contains no records.")
        else:
            st.dataframe(df)
    except Exception as e:
        st.info("No leads database found yet.")