from langchain_openai import OpenAI
import wikipedia

class ResearchAgent:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.llm = OpenAI(model_name=model_name)

    def research(self, topic):
        print(f"[ResearchAgent] Researching topic: {topic}")
        summaries = []
        try:
            pages = wikipedia.search(topic)
            for page in pages[:5]:
                content = wikipedia.summary(page)
                summaries.append({
                    "title": page,
                    "summary": content[:500],
                    "url": f"https://en.wikipedia.org/wiki/{page.replace(' ', '_')}"
                })
        except Exception as e:
            print(f"Error during research: {e}")

        return summaries
