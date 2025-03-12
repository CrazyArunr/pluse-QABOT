# utils/response_handler.py

from models.rag_tool import agent, rag_pipeline, openai_llm

def get_response(query: str) -> str:
    if any(greeting in query.lower() for greeting in ["hi", "hello", "who created you", "who made you"]):
        return "Hello! I was created by the Pulse QA team to assist with testing scenarios and answering questions about the application."
    
    if any(keyword in query.lower() for keyword in ["login", "registration", "profile", "logout", "password"]):
        rag_response = rag_pipeline.run(query)
        bdd_prompt = (
            f"Convert the following steps into BDD (Gherkin) format. "
            f"Do not include technical details like browser actions or locators. "
            f"Focus on the behavior of the system and the user's actions. "
            f"Use the exact locators and steps from the input. "
            f"Do not rephrase or simplify the steps. "
            f"Do not add any extra steps or assumptions. "
            f"Follow this format exactly:\n\n"
            f"Use the following format exactly:\n\n"
            f"Feature: <Feature Name>\n"
            f"Scenario: <Scenario Title>\n"
            f"Given open browser 'chrome'\n"
            f"And navigate to the URL '<URL>'\n"
            f"And maximize the browser window\n"
            f"When enter '<value>' into the element with locator '<locator>'\n"
            f"And enter '<value>' into the element with locator '<locator>'\n"
            f"And enter '<value>' into the element with locator '<locator>'\n"
            f"And click on the element with locator '<locator>'\n"
            f"Then wait for the element with locator '<locator>' to be visible\n"
            f"And the element with locator '<locator>' should have text '<text>'\n\n"
            f"Input:\n{rag_response}"
        )
        bdd_response = openai_llm.predict(bdd_prompt)
        return bdd_response
    else:
        return agent.run(query)