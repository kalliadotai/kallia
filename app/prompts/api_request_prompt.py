API_REQUEST_PROMPT = """You are given the below API Documentation:

{document}

{examples}

Using this documentation, generate the full API url to call for answering the user question.
You should build the API url in order to get a response that is as short as possible, while still getting the necessary information to answer the question.
Pay attention to deliberately exclude any unnecessary pieces of data in the API call.
Wrap the URL in <url> tags.

Question: {question}"""
