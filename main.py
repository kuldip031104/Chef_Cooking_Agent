from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from graph import graph
from database import save_message

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# initial state
state = {
    "messages": [],
    "user_id": "demo_user"
}


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):

    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "messages": state.get("messages", [])
        }
    )


@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):

    global state

    user_id = state["user_id"]

    # add user message to state
    state["messages"].append({
        "role": "user",
        "content": message
    })

    # save user message in DB
    save_message(user_id, "user", message)

    # LangGraph memory config
    config = {
        "configurable": {
            "thread_id": user_id
        }
    }

    # run graph
    updated_state = graph.invoke(state, config=config)

    state.update(updated_state)

    # assistant response
    ai_message = state["messages"][-1]["content"]

    # save assistant message
    save_message(user_id, "assistant", ai_message)

    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "messages": state.get("messages", [])
        }
    )