EXTRACTION_PROMPT = """Your goal is to extract structured information from the user's input that matches the form described below.
When extracting information please make sure it matches the type information exactly.
Do not add any attributes that do not appear in the schema shown below.

{type_description}

Please output the extracted information in JSON format.
Do not output anything except for the extracted information.
Do not add any clarifying information.
Do not add any fields that are not in the schema.
If the text contains attributes that do not appear in the schema, please ignore them.
All output must be in JSON format and follow the schema specified above.

{examples}

Question: {question}"""
