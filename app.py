import uvicorn
from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing_extensions import Annotated

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int
    username: str
    age: int

users = []

@app.get("/", response_class=HTMLResponse, summary="Get Main Page", description="Main page displaying all users.")
async def get_main_page(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users, "user": None})

@app.get("/user/{user_id}", response_class=HTMLResponse, summary="Get User Page", description="Page displaying a specific user's details.")
async def get_user_page(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User not found.")

@app.post("/user/{username}/{age}", summary="Post User", description="Create a new user.")
async def create_user(
    username: Annotated[str, Path(..., min_length=5, max_length=20, description="Enter username", examples="UrbanUser")],
    age: Annotated[int, Path(..., ge=18, le=120, description="Enter age", examples=24)]
) -> User:
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}", summary="Update User", description="Update an existing user's details.")
async def update_user(
    user_id: Annotated[int, Path(..., ge=1, le=100, description="Enter User ID", examples=1)],
    username: Annotated[str, Path(..., min_length=5, max_length=20, description="Enter username", examples="UrbanUser")],
    age: Annotated[int, Path(..., ge=18, le=120, description="Enter age", examples=24)]
) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User not found.")

@app.delete("/user/{user_id}", summary="Delete User", description="Delete a user by ID.")
async def delete_user(
    user_id: Annotated[int, Path(..., ge=1, le=100, description="Enter User ID", examples=1)]
) -> User:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User not found.")

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)