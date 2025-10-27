from langchain_openai import OpenAI

# class CriticAgent:
#     def __init__(self, model_name="gpt-3.5-turbo"):
#         self.llm = OpenAI(model_name=model_name)

#     def critique(self, article):
#         print("[CriticAgent] Reviewing article...")
#         prompt = f"""
#         Review this article for factual accuracy, tone, and missing citations.
#         Provide an improved version followed by a short critique summary.

#         ARTICLE:
#         {article}
#         """
#         return self.llm(prompt)

from langchain_openai import OpenAI

class CriticAgent:
    def __init__(self, model_name="gpt-3.5-turbo"):
        try:
            self.llm = OpenAI(model_name=model_name)
        except Exception as e:
            print("[CriticAgent] Using dummy critic (no API).")
            self.llm = None

    def critique(self, article):
        print("[CriticAgent] Reviewing article...")

        # Dummy fallback if API is not available
        if self.llm is None:
            return "[Dummy Critic] Article looks fine overall, but consider adding more examples and citations."

        prompt = f"""
        Review the following article for:
        - factual accuracy
        - clarity
        - tone and coherence
        - missing citations
        Then suggest improvements and output an improved version.

        ARTICLE:
        {article}
        """

        try:
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            print("[CriticAgent] Error while invoking LLM:", e)
            return f"[CriticAgent ERROR] {e}"
