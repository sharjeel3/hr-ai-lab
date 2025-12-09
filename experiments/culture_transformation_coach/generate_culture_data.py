"""
Generate synthetic culture survey data for testing.
"""

import json
import random
import os
from typing import List, Dict
from datetime import datetime, timedelta


class CultureDataGenerator:
    """Generate synthetic culture survey data."""
    
    CULTURE_DIMENSIONS = [
        "collaboration", "innovation", "accountability",
        "transparency", "work_life_balance", "leadership",
        "diversity_inclusion", "learning_development"
    ]
    
    SURVEY_QUESTIONS = {
        "collaboration": "How well do teams collaborate across departments?",
        "innovation": "Does the organization encourage new ideas and innovation?",
        "accountability": "Are people held accountable for their commitments?",
        "transparency": "How transparent is leadership communication?",
        "work_life_balance": "Does the company support work-life balance?",
        "leadership": "Do you trust and respect leadership?",
        "diversity_inclusion": "Does the company value diversity and inclusion?",
        "learning_development": "Are there opportunities for growth and learning?"
    }
    
    def generate_survey_responses(
        self,
        num_responses: int = 100,
        culture_profile: str = "mixed"
    ) -> List[Dict]:
        """Generate synthetic survey responses."""
        
        responses = []
        
        for i in range(num_responses):
            response = {
                "response_id": f"R{i+1:04d}",
                "timestamp": self._random_timestamp(),
                "department": random.choice([
                    "Engineering", "Sales", "Marketing",
                    "HR", "Finance", "Operations"
                ]),
                "tenure_years": random.uniform(0.5, 15),
                "role_level": random.choice([
                    "Individual Contributor", "Manager",
                    "Senior Manager", "Director", "Executive"
                ]),
                "ratings": self._generate_ratings(culture_profile),
                "open_ended": self._generate_open_ended_response(culture_profile)
            }
            responses.append(response)
        
        return responses
    
    def generate_organization_context(self) -> Dict:
        """Generate organization context."""
        
        return {
            "company_size": random.choice(["startup", "mid_size", "enterprise"]),
            "industry": random.choice([
                "Technology", "Healthcare", "Finance",
                "Retail", "Manufacturing"
            ]),
            "stated_values": [
                "Innovation", "Integrity", "Customer Focus",
                "Collaboration", "Excellence"
            ],
            "recent_changes": random.choice([
                ["Leadership change", "Reorganization"],
                ["Rapid growth", "New product launch"],
                ["Merger/acquisition", "Market challenges"],
                []
            ]),
            "current_initiatives": [
                "DEI program", "Remote work policy",
                "Learning platform rollout"
            ]
        }
    
    def _generate_ratings(self, profile: str) -> Dict:
        """Generate dimension ratings based on profile."""
        
        ratings = {}
        
        for dimension in self.CULTURE_DIMENSIONS:
            if profile == "positive":
                base_score = random.uniform(7, 10)
            elif profile == "negative":
                base_score = random.uniform(3, 6)
            else:  # mixed
                base_score = random.uniform(4, 9)
            
            ratings[dimension] = {
                "score": round(base_score, 1),
                "question": self.SURVEY_QUESTIONS[dimension]
            }
        
        return ratings
    
    def _generate_open_ended_response(self, profile: str) -> str:
        """Generate open-ended survey response."""
        
        positive_comments = [
            "Great team culture and supportive leadership.",
            "I feel valued and have opportunities to grow.",
            "Innovation is truly encouraged here.",
            "Work-life balance is respected.",
        ]
        
        negative_comments = [
            "Communication from leadership could be better.",
            "Limited opportunities for career advancement.",
            "Too much bureaucracy slows down innovation.",
            "Work-life balance is challenging.",
        ]
        
        neutral_comments = [
            "Some good aspects, but room for improvement.",
            "Depends on which team you're on.",
            "Getting better but still a work in progress.",
        ]
        
        if profile == "positive":
            return random.choice(positive_comments)
        elif profile == "negative":
            return random.choice(negative_comments)
        else:
            return random.choice(neutral_comments + positive_comments + negative_comments)
    
    def _random_timestamp(self) -> str:
        """Generate random timestamp within last 30 days."""
        
        days_ago = random.randint(0, 30)
        timestamp = datetime.now() - timedelta(days=days_ago)
        return timestamp.isoformat()


if __name__ == "__main__":
    generator = CultureDataGenerator()
    
    # Generate survey data
    responses = generator.generate_survey_responses(num_responses=150)
    context = generator.generate_organization_context()
    
    # Save to file
    output_dir = "../../datasets/culture_surveys"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/survey_responses.json", "w") as f:
        json.dump(responses, f, indent=2)
    
    with open(f"{output_dir}/organization_context.json", "w") as f:
        json.dump(context, f, indent=2)
    
    print(f"Generated {len(responses)} survey responses")
    print(f"Saved to {output_dir}/")
