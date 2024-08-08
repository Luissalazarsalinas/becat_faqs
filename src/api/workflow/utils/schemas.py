from pydantic import BaseModel

class FaqsRequest(BaseModel):
    question : str