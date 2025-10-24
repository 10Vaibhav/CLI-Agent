from pydantic import BaseModel, Field
from typing import Optional

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: PLAN, OUTPUT, TOOL, etc")
    content: Optional[str] = Field(None, description="The optional string content for the step")
    tool: Optional[str] = Field(None, description="The ID of the tool to call")
    input: Optional[str] = Field(None, description="The input params for the tool")
    output: Optional[str] = Field(None, description="output of the tool")

