from pydantic import BaseModel, Field
from typing import Dict

class CarteiraWeights(BaseModel):
    tickers_weights: Dict[str, float] = Field(description="Tickers and their respective weights. The sum of the weights should be 100.")
    justification : str = Field(description="Justification about the allocation. Explain why the weights of each asset are chosen.",
                                max_length=1000)