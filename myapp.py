from fastapi import FastAPI
from starlette.responses import FileResponse
from fastapi.responses import FileResponse


app=FastAPI()
app.mount("/", static_files_directory="public", static_files_url="/")
if not  os.path.exists("session"):
    os.makedirs("session")
@app.get("/")
def root():
    return{"message":"Hello world"}
@app.get("/users")
def get_users():
    return[{"id":1,"name":"me"}]
if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)
@app.post("/api/users")
def create_session():
    print("create_session")
