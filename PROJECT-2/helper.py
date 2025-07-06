from pydantic import BaseModel, Field

from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# class TableInfo(BaseModel):
#     name: str = Field(description="The name of the table")
#     column_names: List[str] = Field(description="List of column names")
#     datatypes: Dict[str, str] = Field(description="Mapping of column name to data type")
#     primary_key: List[str] = Field(description="List of primary key columns")
#     foreign_keys: Optional[List[str]] = Field(default=[], description="List of foreign key definitions")
#     sequences: Optional[List[str]] = Field(default=[], description="List of sequences if any")
#     constraints: Optional[List[str]] = Field(default=[], description="List of constraints on table")

# class ResponseFormatter(BaseModel):
#     # schema_name: str = Field(description="The name of the schema")
#     # enum_names: Optional[List[str]] = Field(description="List of all enum names")
#     # table_names: Optional[List[str]] = Field(description="List of all table names")
#     # tables_info: Optional [Dict[str, TableInfo]] = Field(description="A mapping from table name to its metadata")
#     answer: str = Field(description="The answer to the user's question")
#     followup_question: str = Field(description="A followup question the user could ask")

def system_message():
    return """
    Your name is Alexender, a virtual assistant skilled in database-related tasks, especially fetching and summarizing schema-level details.
    When a user asks you a question, use tools as needed to gather schema information. Then, return your response using the structured format defined in the `ResponseFormatter` schema.
    Always return a response using this format:
    
    - answer: A clear and structured JSON response containing details for each table. Each table should include:
     - schema_name: Name of the schema
        - name: Name of the table
        - column_names: List of all column names
        - datatypes: Dictionary mapping each column name to its datatype
        - primary_key: List of primary key columns
        - foreign_keys: List of foreign key descriptions
        - sequences: Any sequences associated with the table
        - constraints: List of table constraints (e.g., check constraints, uniqueness, etc.)
    """
