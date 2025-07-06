import json
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

# class DBConnectionResponse(BaseModel):
#     connection_status: bool = Field(..., description="True if DB connection is successful, otherwise false")
#     error_message: str = Field(..., description="Error message if any")

def SystemMessage():
    system_message = [
        """
        You are an agent named DBConnector, and task is to check if connection to DB can be made or not.
        Return a response using the following format strictly, avoid any other text:

        response: 
            connection_status: true or false
            error_message: if any
        """,

        """
        Your name is SchemaGPT, a virtual assistant skilled in database-related tasks, especially fetching and summarizing schema-level details.
        When a user asks you a question, use tools as needed to gather schema information. Then, return your response using the structured format defined in the `ResponseFormatter` schema.
        Always return a response using this format:
        
        - response: A clear and structured JSON response containing details for each table. Each table should include:
            - schema_name: Name of the schema
                - name: Name of the table
                - column_names: List of all column names
                - datatypes: Dictionary mapping each column name to its datatype
                - primary_key: List of primary key columns
                - foreign_keys: List of foreign key descriptions
                - sequences: Any sequences associated with the table
                - constraints: List of table constraints (e.g., check constraints, uniqueness, etc.)

        - example:
            response:
                schema_name: public
                    name: stock
                    column_names: ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']
                    datatypes: {'symbol': 'character varying', 'date': 'date', 'open': 'numeric', 'high': 'numeric', 'low': 'numeric', 'close': 'numeric', 'volume': 'numeric'}
                    primary_key: ['symbol', 'date']
                    foreign_keys: []
                    sequences: []
                    constraints: ['stock_pk PRIMARY KEY (symbol, date)']

                    name: owner
                    column_names: ['id', 'name']
                    datatypes: {'id': 'integer', 'name': 'character varying'}
                    primary_key: ['id']
                    foreign_keys: []
                    sequences: []
                    constraints: ['owner_pkey PRIMARY KEY (id)']

        """
    ]
    return system_message

def HumanMesssage():
    human_message = [
        "Connect to the database and check it is connected sussessfully or not, If there is any error, print that..!",
        "Give me a full JSON summary of the database schema. If there is any error, print that..!",
        "Check if there is a table called 'stock'. If there is, can you tell me how many columns are there in the table called 'stock'? If there is not, can you tell me why? If there is, Can you tell me how many rows are there in the table called '{table_name}'?"
    ]
    return human_message

def ParseDbConnectAgentResponse(response):
    try:
        result = json.loads(response)
        connection_status = result.get("connection_status", False)
        error_message = result.get("error_message", "")
        print("✅ Connection Status:", connection_status)
        print("✅ Error Message:", error_message)
        return connection_status

    except json.JSONDecodeError:
        print("❌ Failed to parse connection response and ErrorMessage as JSON.")
        return False