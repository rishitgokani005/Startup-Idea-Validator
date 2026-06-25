import os
import re
from typing import Dict, List, Optional
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class Agent:
    def __init__(self, name: str, role: str, system_prompt: str, temperature: float = 0.7):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"

    def execute(self, idea_context: str) -> Dict:
        """Executes the agent's logic based on the provided idea context."""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Evaluate this startup idea:\n\n{idea_context}"}
                ],
                model=self.model,
                temperature=self.temperature,
            )
            response_text = chat_completion.choices[0].message.content
            score = self._extract_score(response_text)
            
            return {
                "agent_name": self.name,
                "role": self.role,
                "report": response_text,
                "score": score
            }
        except Exception as e:
            return {
                "agent_name": self.name,
                "role": self.role,
                "report": f"Error during execution: {str(e)}",
                "score": 0
            }

    def _extract_score(self, text: str) -> int:
        """Extracts an integer score out of 100 from the agent's report."""
        # Look for patterns like "SCORE: 85" or "85/100"
        match = re.search(r"SCORE:\s*(\d+)", text, re.IGNORECASE)
        if match:
            return min(100, max(0, int(match.group(1))))
        
        match = re.search(r"(\d+)/100", text)
        if match:
            return min(100, max(0, int(match.group(1))))
            
        return 50  # Default neutral score if not found

class SpecializedAgents:
    @staticmethod
    def get_skeptical_vc() -> Agent:
        return Agent(
            name="Skeptical VC Investor",
            role="Market & Financial Viability",
            system_prompt=(
                "You are an elite, highly skeptical Venture Capitalist from a top-tier firm. "
                "Your job is to find reasons NOT to invest. Focus on: "
                "1. Total Addressable Market (TAM) - is it actually big enough? "
                "2. Unit Economics - will this ever be profitable? "
                "3. Scalability - can it grow without linear cost increases? "
                "4. Moat/Defensibility - why won't Google/Amazon crush them? "
                "5. Exit Strategy - who buys this? "
                "Be critical, direct, and professional. You must end your report with 'SCORE: X' where X is 0-100."
            )
        )

    @staticmethod
    def get_target_customer() -> Agent:
        return Agent(
            name="The Target Customer",
            role="Problem-Solution Fit",
            system_prompt=(
                "You are the ideal target customer for this idea. You are busy, picky, and tired of 'solutions' "
                "that create more problems. Focus on: "
                "1. Real-world pain - does this solve a problem I have every day? "
                "2. Willingness to pay - would I actually open my wallet? "
                "3. Onboarding friction - is it too hard to start? "
                "4. Habit forming - will I use this a month from now? "
                "Be honest and skeptical. If it's a 'vitamin' instead of a 'painkiller', say so. "
                "You must end your report with 'SCORE: X' where X is 0-100."
            )
        )

    @staticmethod
    def get_growth_expert() -> Agent:
        return Agent(
            name="Growth & Marketing Guru",
            role="GTM & Distribution",
            system_prompt=(
                "You are a legendary Growth Hacker who has scaled 3 unicorns. "
                "Focus on: "
                "1. Customer Acquisition Cost (CAC) vs Life-Time Value (LTV). "
                "2. Distribution Channels - where are the users? "
                "3. Virality - is there a built-in referral loop? "
                "4. Go-To-Market (GTM) strategy - how do we win the first 1000 users? "
                "Identify potential 'death valleys' in growth. "
                "You must end your report with 'SCORE: X' where X is 0-100."
            )
        )

    @staticmethod
    def get_technical_architect() -> Agent:
        return Agent(
            name="Technical Architect",
            role="Feasibility & Infrastructure",
            system_prompt=(
                "You are a seasoned CTO and Technical Architect. "
                "Focus on: "
                "1. Technical Feasibility - can this actually be built? "
                "2. Architectural Bottlenecks - what breaks at 1M users? "
                "3. Data Dependencies - do we need data we don't have? "
                "4. Complexity vs Timeline - is this a 6-month or a 6-year project? "
                "5. Scaling Costs - will AWS bills kill the margin? "
                "Be pragmatic and alert to 'vaporware' or over-engineered solutions. "
                "You must end your report with 'SCORE: X' where X is 0-100."
            )
        )

class InputValidatorAgent:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"

    def is_valid(self, title: str, audience: str, description: str) -> Dict:
        """Checks if the input describes a potentially valid startup idea or if it's gibberish/invalid."""
        prompt = (
            "You are a gatekeeper for a startup validation tool. Your task is to determine if the following input "
            "is a legitimate startup idea or just gibberish, random characters, or completely nonsensical text.\n\n"
            f"Title: {title}\n"
            f"Target Audience: {audience}\n"
            f"Description: {description}\n\n"
            "Rules:\n"
            "1. If it looks like a real attempt at a startup idea (even a bad one), return 'VALID'.\n"
            "2. If it is random characters (e.g., 'ejoiejoia'), single word spam, incoherent rambling, or offensive non-startup content, return 'INVALID' followed by a short reason why it was rejected.\n"
            "3. Format: 'STATUS: VALID' or 'STATUS: INVALID | Reason: [short reason]'"
        )

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.1,
            )
            response = chat_completion.choices[0].message.content
            if "STATUS: VALID" in response:
                return {"is_valid": True}
            else:
                reason_match = re.search(r"Reason:\s*(.*)", response)
                reason = reason_match.group(1) if reason_match else "Incoherent or invalid input detected."
                return {"is_valid": False, "reason": reason}
        except Exception:
            # Fallback to basic length/pattern check if API fails
            if len(description) < 10 or len(title) < 2:
                return {"is_valid": False, "reason": "Input is too short to be a valid idea."}
            return {"is_valid": True}
class SynthesizerAgent:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"

    def synthesize(self, idea_context: str, individual_reports: List[Dict]) -> Dict:
        """Conducts a consensus review and generates an Executive Summary."""
        reports_summary = "\n\n".join([
            f"--- AGENT: {r['agent_name']} (Score: {r['score']}) ---\n{r['report']}"
            for r in individual_reports
        ])
        
        system_prompt = (
            "You are the Lead Investment Committee Chair. You have read four specialized reports "
            "on a new startup idea. Your job is to: "
            "1. Highlight the key points of agreement and disagreement among the agents. "
            "2. Conduct a mock 'consensus review'. "
            "3. Calculate a final weighted average validation score (give more weight to the VC and Customer feedback). "
            "4. Provide a clear 'GO' or 'NO-GO' recommendation with an Executive Summary. "
            "End your summary with 'FINAL SCORE: X' where X is 0-100."
        )

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Startup Idea: {idea_context}\n\nIndividual Reports:\n{reports_summary}"}
                ],
                model=self.model,
                temperature=0.5,
            )
            response_text = chat_completion.choices[0].message.content
            
            # Extract final score
            match = re.search(r"FINAL SCORE:\s*(\d+)", response_text, re.IGNORECASE)
            final_score = int(match.group(1)) if match else sum(r['score'] for r in individual_reports) // len(individual_reports)

            return {
                "executive_summary": response_text,
                "final_score": final_score
            }
        except Exception as e:
            return {
                "executive_summary": f"Synthesis failed: {str(e)}",
                "final_score": 0
            }

def run_validation_pipeline(idea_title: str, target_audience: str, description: str):
    """Orchestrates the entire multi-agent validation loop."""
    
    # --- Step 0: Input Validation ---
    validator = InputValidatorAgent()
    validation_status = validator.is_valid(idea_title, target_audience, description)
    
    if not validation_status["is_valid"]:
        raise ValueError(f"Invalid Startup Idea: {validation_status['reason']}")

    idea_context = f"Title: {idea_title}\nTarget Audience: {target_audience}\nDescription: {description}"

    
    agents = [
        SpecializedAgents.get_skeptical_vc(),
        SpecializedAgents.get_target_customer(),
        SpecializedAgents.get_growth_expert(),
        SpecializedAgents.get_technical_architect()
    ]
    
    individual_results = []
    for agent in agents:
        # In a real production app, you might run these in parallel
        # For clarity and ordered logs, we'll run them sequentially
        result = agent.execute(idea_context)
        individual_results.append(result)
    
    synthesizer = SynthesizerAgent()
    summary = synthesizer.synthesize(idea_context, individual_results)
    
    return {
        "idea_title": idea_title,
        "individual_reports": individual_results,
        "executive_summary": summary["executive_summary"],
        "final_score": summary["final_score"]
    }
