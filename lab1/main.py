from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/")
def root():
    return Response(status_code=200)

@app.post("/post")
def handle_post():
    return Response(status_code=200)

@app.delete("/delete")
def handle_post():
    return Response(status_code=200)