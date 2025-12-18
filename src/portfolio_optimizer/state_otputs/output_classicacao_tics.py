from typing import Literal
from pydantic import BaseModel, Field

class TickerLevel(BaseModel):
    classification: Literal["Excellent","Good", "Fair", "Poor", "Very Poor"] = Field(
        description="Ticker classification. Can be 'Excellent', 'Good', 'Fair', 'Poor', or 'Very Poor'. Respond in Inglish."
    )
    analysis: str = Field(
        description="Arguments justifying the classification given to the ticker.",
        max_length=1000
    )
    
class SeniorAvaliador(BaseModel):
    """Specific issue found in the analysis."""
    
    avaliacao_analise: Literal[True, False] = Field(
        description="Evaluation of the analyst's analysis, indicating if it is True (that a good analisy) or False (that is a bad analisy)."
    )
    
    description_avaliacao_analise: str = Field(
        description="Detailed description of the avaliation. Why you think that.",
        max_length=1000
    )