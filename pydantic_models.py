from pydantic import BaseModel


class MetadataSchema(BaseModel):
    country: str
    project: str
    program: str
    theme: str
    year: str
    risk: str
    severity: str
    status: str


class OutputSchema(BaseModel):
    fixed_data: str
    summary: str
