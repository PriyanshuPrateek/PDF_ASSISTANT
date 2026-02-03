def build_prompt(chat_history, context, query):
    return f"""
    You are an intelligent research assistant.

    Previous Conversation:
    {chat_history}

    Answer the question using the provided document as the primary source of context.
  If the document does not explicitly contain the answer, you may use relevant external knowledge only if the question is clearly aligned with the document’s subject matter.
  If the question is not relevant to the document, respond exactly with:
  ‘I could not find the answer in the provided document.’
  Do not introduce unrelated information.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """
