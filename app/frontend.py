import streamlit as st
import requests
import json
import time

# Page Config
st.set_page_config(
    page_title="Startup Validator | Multi-Agent Analysis",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.02);
    }
    .metric-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363d;
        text-align: center;
    }
    .agent-header {
        color: #58a6ff;
        font-weight: bold;
    }
    .score-high {
        color: #3fb950;
        font-size: 24px;
        font-weight: bold;
    }
    .score-med {
        color: #d29922;
        font-size: 24px;
        font-weight: bold;
    }
    .score-low {
        color: #f85149;
        font-size: 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🚀 Multi-Agent Startup Idea Validator")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("Idea Details")
        st.info("Fill in the details below to trigger an elite multi-agent audit of your startup concept.")
        
        with st.form("idea_form"):
            idea_title = st.text_input("Startup Name", placeholder="e.g. Uber for Pet Care")
            target_audience = st.text_input("Target Audience", placeholder="e.g. Busy young professionals in metropolitan areas")
            detailed_description = st.text_area("Core Mechanism / Description", placeholder="Explain how it works, what the pain point is, and how you solve it...", height=200)
            
            submit_button = st.form_submit_button("Execute Validation Audit")

    with col2:
        st.header("Validation Dashboard")
        
        if submit_button:
            if not idea_title or not detailed_description:
                st.error("Please provide both a title and a description.")
            else:
                progress_placeholder = st.empty()
                status_placeholder = st.empty()
                
                # Visual step tracker
                steps = [
                    "Skeptical VC is analyzing market size...",
                    "Target Customer is evaluating pain-point fit...",
                    "Growth Expert is calculating CAC/LTV paths...",
                    "Technical Architect is reviewing feasibility...",
                    "Synthesizer Agent is compiling final verdict..."
                ]
                
                try:
                    from app.agents import run_validation_pipeline
                except ImportError:
                    from agents import run_validation_pipeline

                try:
                    with st.spinner("Agents are debating..."):
                        # Simulate visual progress for better UX
                        for i, step in enumerate(steps):
                            status_placeholder.write(f"🔍 **Step {i+1}:** {step}")
                            time.sleep(0.5) # Small delay for visual effect
                            
                        # Direct call to the validation pipeline
                        data = run_validation_pipeline(
                            idea_title=idea_title,
                            target_audience=target_audience,
                            description=detailed_description
                        )
                        
                        status_placeholder.empty()
                        display_results(data)
                except Exception as e:
                    st.error(f"Validation failed: {str(e)}")
                    st.info("Check your GROQ_API_KEY and internet connection.")
        else:
            st.write("Results will appear here after execution.")
            st.image("https://img.freepik.com/free-vector/growth-concept-illustration_114360-1282.jpg", width=400)

def display_results(data):
    # Summary Section
    st.success("Validation Audit Complete!")
    
    score = data['final_score']
    score_class = "score-high" if score >= 70 else ("score-med" if score >= 40 else "score-low")
    
    col_a, col_b = st.columns([1, 3])
    with col_a:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Aggregate Score</h3>
            <span class="{score_class}">{score}/100</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.subheader("Executive Summary")
        st.markdown(data['executive_summary'])

    st.markdown("---")
    st.header("Detailed Agent Reports")
    
    # Tabs for individual reports
    tabs = st.tabs([r['agent_name'] for r in data['individual_reports']])
    
    for i, report in enumerate(data['individual_reports']):
        with tabs[i]:
            score_val = report['score']
            s_class = "score-high" if score_val >= 70 else ("score-med" if score_val >= 40 else "score-low")
            
            st.markdown(f"**Role:** {report['role']}")
            st.markdown(f"**Agent Score:** <span class='{s_class}'>{score_val}/100</span>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown(report['report'])

if __name__ == "__main__":
    main()
