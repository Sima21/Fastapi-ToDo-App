import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import mysql.connector

app = FastAPI()
templates = Jinja2Templates(directory="src/templates")

# Database connection details
db_config = {
    "host": "localhost",
    "user": "todo_user",
    "password": "ToDoList2023!",
    "database": "todo_app",
}

# Mount the "static" directory as a static directory
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Establish a database connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # Fetch data from the database
    query = "SELECT * FROM todos;"
    cursor.execute(query)
    result = cursor.fetchall()

    # Extract column names
    columns = [desc[0] for desc in cursor.description]

    # Combine column names and rows into a list of dictionaries
    data = [dict(zip(columns, row)) for row in result]

    # Construct the relative path to the template file
    template_path = "index.html"
    return templates.TemplateResponse(template_path, {"request": request, "data": data})

@app.post("/save-task/")
async def save_task(request: Request, task: str = Form(...)):
    try:
        # Update the query to use the correct column names
        query = "INSERT INTO todos (`Todoitem`, `Status`) VALUES (%s, 'open');"

        # Create a buffered cursor
        cursor_insert = conn.cursor(buffered=True)

        # Execute the query with the task_name parameter
        cursor_insert.execute(query, (task,))
        conn.commit()

        # Close the cursor after the query
        cursor_insert.close()
        response = RedirectResponse(url="http://localhost:8000/", status_code=302)
        return response
        # return {"message": "Task saved successfully!"}

    except Exception as e:
        return {"message": f"Error saving task: {str(e)}"}
    
@app.post("/delete")
async def delete_task(request: Request, No: list = Form(...)):
    try:
        # Update the query to delete the task by task_id
        query = "DELETE FROM todos WHERE No = %s;"

        # Create a buffered cursor
        cursor_delete = conn.cursor(buffered=True)

        # Execute the query with the task_id parameter
        cursor_delete.execute(query, (No))
        conn.commit()
        print(No)
        # Close the cursor after the query
        cursor_delete.close()

        response = RedirectResponse(url="http://localhost:8000/", status_code=302)
        return response
    except Exception as e:
        return {"message": f"Error deleting task: {str(e)}"}
    
@app.post("/update")
async def update_status(request: Request, No: list = Form(...)):
    try:
        query = "UPDATE todos SET Status = 'in progress' WHERE No = %s;"
        cursor_update = conn.cursor(buffered=True)
        cursor_update.execute(query, (No))
        conn.commit()
        cursor_update.close
        response = RedirectResponse(url="http://localhost:8000/", status_code=302)
        return response
    except Exception as e:
        return {"message": f"Error updating task: {str(e)}"}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
