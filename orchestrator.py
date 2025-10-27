
import os
import sys
import json
import datetime
import traceback


# Try to import agent classes — give a helpful error if they are missing
try:
    from research_agent import ResearchAgent
    from writer_agent import WriterAgent
    from critic_agent import CriticAgent
except Exception as e:
    print("ERROR: Could not import agent modules. Make sure these files exist in the same folder:")
    print(" - research_agent.py (class ResearchAgent)")
    print(" - writer_agent.py  (class WriterAgent)")
    print(" - critic_agent.py  (class CriticAgent)")
    print("\nDetailed import error:")
    traceback.print_exc()
    raise SystemExit(1)


# Logging helper
def log_interaction(agent_name: str, message: str):
    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_message = message if isinstance(message, str) else json.dumps(message, indent=2, ensure_ascii=False)
    log_line = f"[{timestamp}] {agent_name}:\n{safe_message}\n\n"
    with open(os.path.join("outputs", "logs.txt"), "a", encoding="utf-8") as f:
        f.write(log_line)


def save_final_article(text: str):
    os.makedirs("outputs", exist_ok=True)
    out_path = os.path.join("outputs", "final_article.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"\n✅ Final article saved to: {out_path}")


def safe_str(x):
    try:
        return str(x)
    except:
        return json.dumps(x, default=str, ensure_ascii=False)


def main():
    print("=== Agentic AI — Orchestrator ===\n")
    # Get topic from user
    topic = input("Enter your topic (e.g. 'The future of Agentic AI and autonomous systems'):\n> ").strip()
    if not topic:
        print("No topic entered. Exiting.")
        return

    # Instantiate agents
    try:
        research_agent = ResearchAgent()
    except Exception as e:
        print("Failed to create ResearchAgent. See error below:")
        traceback.print_exc()
        return

    try:
        writer_agent = WriterAgent()
    except Exception as e:
        print("Failed to create WriterAgent. See error below:")
        traceback.print_exc()
        return

    try:
        critic_agent = CriticAgent()
    except Exception as e:
        print("Failed to create CriticAgent. See error below:")
        traceback.print_exc()
        return

    # Step 1: Research
    print("\n[1/3] Research agent running...")
    try:
        research_results = research_agent.research(topic)
        print(f"Research complete — {len(research_results) if hasattr(research_results, '__len__') else 'unknown'} items returned.")
        log_interaction("ResearchAgent", safe_str(research_results))
    except Exception as e:
        print("ResearchAgent raised an error:")
        traceback.print_exc()
        log_interaction("ResearchAgent", f"ERROR: {safe_str(traceback.format_exc())}")
        return

    # Step 2: Writer
    print("\n[2/3] Writer agent running...")
    try:
        # Many writer agents expect research snippets as a list; if your research agent returns dict, pass as-is.
        draft_article = writer_agent.write_article(topic, research_results)
        if not isinstance(draft_article, str):
            draft_article = safe_str(draft_article)
        print("WriterAgent produced a draft.")
        log_interaction("WriterAgent", draft_article[:3000])  # save first N chars so logs don't explode
    except Exception as e:
        print("WriterAgent raised an error:")
        traceback.print_exc()
        log_interaction("WriterAgent", f"ERROR: {safe_str(traceback.format_exc())}")
        return

    # Step 3: Critic
    print("\n[3/3] Critic/Editor agent running...")
    try:
        critique_output = critic_agent.critique(draft_article)
        if not isinstance(critique_output, str):
            critique_output = safe_str(critique_output)
        print("CriticAgent finished.")
        log_interaction("CriticAgent", critique_output[:3000])
    except Exception as e:
        print("CriticAgent raised an error:")
        traceback.print_exc()
        log_interaction("CriticAgent", f"ERROR: {safe_str(traceback.format_exc())}")
        return

    # Save final result (critic may return improved draft or a dict with keys)
    # Try to find improved article text inside critique_output if it's a dict-like string
    final_text = critique_output
    # If critic returns JSON-like string with keys, try to parse
    try:
        parsed = None
        if isinstance(critique_output, str):
            # try JSON parse
            try:
                parsed = json.loads(critique_output)
            except:
                parsed = None
        if isinstance(parsed, dict):
            # common keys: "improved_article", "final", "article"
            for key in ("improved_article", "final_article", "final", "article", "improved"):
                if key in parsed:
                    final_text = parsed[key]
                    break
    except Exception:
        pass

    # If final_text is still not a string, convert
    final_text = final_text if isinstance(final_text, str) else safe_str(final_text)

    save_final_article(final_text)

    print("\nAll done. Logs are in 'outputs/logs.txt'.")
    print("Open outputs/final_article.txt to read your article.\n")


if __name__ == "__main__":
    main()
