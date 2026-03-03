from langchain_groq import ChatGroq
from pydantic import BaseModel
from Prompts.persona import CHEF_SYSTEM_PROMPT
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

class RecipeOutput(BaseModel):
    recipe_name: str
    cultural_story: str
    ingredients: list[str]
    method: list[str]
    chef_tips: str
    substitutions: str

def recipe_agent(state):

    prompt = f"""
    {CHEF_SYSTEM_PROMPT}

    People: {state['number_of_people']}
    Spice: {state['spice_level']}
    Region: {state['region_preference']}
    """

    result = llm.with_structured_output(RecipeOutput).invoke(prompt)

    return {
        "recipe": result.dict(),
        "steps": result.method,
        "current_step": 0,
        "messages": [{
            "role": "assistant",
            "content": f"""
🍲 {result.recipe_name}

{result.cultural_story}

Ingredients:
{chr(10).join(result.ingredients)}

Would you like step-by-step guidance?
"""
        }]
    }