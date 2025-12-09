"""
Experiment H: Culture Transformation Coach
Analyzes organizational culture and provides actionable transformation guidance.
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()


class CultureTransformationCoach:
    """AI coach for organizational culture transformation."""
    
    def __init__(self, model: str = "gemini-2.0-flash-exp"):
        """Initialize the culture coach."""
        self.model = model
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.client = genai.GenerativeModel(model)
        
    def analyze_culture_survey(
        self,
        survey_responses: List[Dict],
        organization_context: Optional[Dict] = None
    ) -> Dict:
        """Analyze culture survey responses and identify patterns."""
        
        prompt = self._build_analysis_prompt(survey_responses, organization_context)
        
        response = self.client.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=4000,
                temperature=0.7
            )
        )
        
        analysis = self._parse_analysis(response.text)
        return analysis
    
    def generate_transformation_plan(
        self,
        culture_analysis: Dict,
        goals: List[str],
        constraints: Optional[Dict] = None
    ) -> Dict:
        """Generate a detailed culture transformation plan."""
        
        prompt = self._build_transformation_prompt(
            culture_analysis, goals, constraints
        )
        
        response = self.client.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=4000,
                temperature=0.7
            )
        )
        
        plan = self._parse_transformation_plan(response.text)
        return plan
    
    def provide_coaching_guidance(
        self,
        scenario: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """Provide coaching guidance for specific cultural scenarios."""
        
        prompt = f"""As a culture transformation coach, provide guidance for this scenario:

Scenario: {scenario}

Context: {json.dumps(context, indent=2) if context else 'None provided'}

Provide:
1. Analysis of the cultural implications
2. Recommended approaches
3. Potential challenges
4. Success metrics
5. Timeline expectations

Format your response as structured JSON."""

        response = self.client.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=3000,
                temperature=0.7
            )
        )
        
        guidance = self._parse_guidance(response.text)
        return guidance
    
    def assess_culture_health(
        self,
        metrics: Dict,
        historical_data: Optional[List[Dict]] = None
    ) -> Dict:
        """Assess overall culture health based on metrics."""
        
        prompt = f"""Assess organizational culture health based on these metrics:

Current Metrics:
{json.dumps(metrics, indent=2)}

Historical Data:
{json.dumps(historical_data, indent=2) if historical_data else 'Not available'}

Provide a comprehensive health assessment including:
1. Overall health score (0-100)
2. Strengths by dimension
3. Areas of concern
4. Trend analysis
5. Risk factors
6. Recommended interventions

Format as structured JSON."""

        response = self.client.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=3000,
                temperature=0.7
            )
        )
        
        assessment = self._parse_assessment(response.text)
        return assessment
    
    def _build_analysis_prompt(
        self,
        responses: List[Dict],
        context: Optional[Dict]
    ) -> str:
        """Build prompt for culture analysis."""
        
        prompt = f"""Analyze these organizational culture survey responses:

Survey Responses ({len(responses)} responses):
{json.dumps(responses[:50], indent=2)}  # Limit for token management

Organization Context:
{json.dumps(context, indent=2) if context else 'Not provided'}

Provide a comprehensive analysis including:
1. Key themes and patterns
2. Cultural strengths
3. Areas for improvement
4. Employee sentiment analysis
5. Subgroup variations (if detectable)
6. Underlying cultural values
7. Alignment with stated values

Format your response as structured JSON with these sections."""

        return prompt
    
    def _build_transformation_prompt(
        self,
        analysis: Dict,
        goals: List[str],
        constraints: Optional[Dict]
    ) -> str:
        """Build prompt for transformation plan generation."""
        
        prompt = f"""Based on this culture analysis, create a transformation plan:

Culture Analysis:
{json.dumps(analysis, indent=2)}

Transformation Goals:
{json.dumps(goals, indent=2)}

Constraints:
{json.dumps(constraints, indent=2) if constraints else 'None specified'}

Create a detailed transformation plan with:
1. Executive summary
2. Phased approach (short, medium, long-term)
3. Specific initiatives per phase
4. Resource requirements
5. Success metrics and KPIs
6. Risk mitigation strategies
7. Communication strategy
8. Quick wins
9. Expected outcomes

Format as structured JSON."""

        return prompt
    
    def _parse_analysis(self, text: str) -> Dict:
        """Parse culture analysis from LLM response."""
        try:
            # Try to extract JSON
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
        
        # Fallback to structured text parsing
        return {
            "raw_analysis": text,
            "timestamp": datetime.now().isoformat(),
            "parsed": False
        }
    
    def _parse_transformation_plan(self, text: str) -> Dict:
        """Parse transformation plan from LLM response."""
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
        
        return {
            "raw_plan": text,
            "timestamp": datetime.now().isoformat(),
            "parsed": False
        }
    
    def _parse_guidance(self, text: str) -> Dict:
        """Parse coaching guidance from LLM response."""
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
        
        return {
            "raw_guidance": text,
            "timestamp": datetime.now().isoformat(),
            "parsed": False
        }
    
    def _parse_assessment(self, text: str) -> Dict:
        """Parse health assessment from LLM response."""
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
        
        return {
            "raw_assessment": text,
            "timestamp": datetime.now().isoformat(),
            "parsed": False
        }
