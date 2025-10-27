from langchain_openai import OpenAI

# class WriterAgent:
#     def __init__(self, model_name="gpt-3.5-turbo"):
#         # Initialize the LLM
#         self.llm = OpenAI(model=model_name)

#     def write_article(self, topic, research_snippets):
#         print("[WriterAgent] Writing article...")

#         # Combine all research summaries
#         combined_text = "\n".join([r["summary"] for r in research_snippets if "summary" in r])

#         # Prepare the prompt
#         prompt = f"""
#         Write a detailed 700-1200 word article about '{topic}'.
#         Use the following research summaries:
#         {combined_text}
#         Include citations and structure it like a professional blog post.
#         """

#         # ✅ Use .invoke() instead of calling the object directly
#         response = self.llm.invoke(prompt)

#         # Return the generated text
#         return response


class DummyWriter:
    def invoke(self, prompt):
        return f"[Dummy Article] This is a placeholder article for: {prompt[:50]}..."

class WriterAgent:
    def __init__(self, model_name=None):
        self.llm = DummyWriter()

    def write_article(self, topic, research_snippets):
        print("[WriterAgent] Writing dummy article (no API)...")
        combined_text = "\n".join([r.get("summary", "") for r in research_snippets])
        prompt = f"Write about '{topic}' using these points:\n{combined_text}"
        return self.llm.invoke(prompt)
