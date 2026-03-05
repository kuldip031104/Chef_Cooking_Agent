from fastapi import FastAPI,Request,Form
from database import save_message
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from graph import graph

app = FastAPI()

templates = Jinja2Templates(directory="templates")

state ={
    "message":[],
    "user_id":"demo_user"
}

@app.get("/",response_class=HTMLResponse)

async def Chat_page(request:Request):
    return templates.TemplateResponse(
        "chat.html",
        {"request":request,
         "messages":state.get("message",[])
        }
    )
    
@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):

    global state

    # Ensure messages key exists
    if "messages" not in state:
        state["messages"] = []

    state["messages"].append({
        "role": "user",
        "content": message
    })
    # Human message
    save_message(state['user_id'],"user",message)

    updated_state = graph.invoke(state)

    state.update(updated_state)
    # ai_message
    ai_message = state['messages'][-1]['content']
    save_message(state['user_id'],'assistant',ai_message)

    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "messages": state.get("messages", [])}
    )