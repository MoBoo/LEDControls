from fastapi import FastAPI, status, Request, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/pattern")
async def post_pattern(request: Request):
  return Response(status_code=status.HTTP_200_OK)


@app.post("/brightness")
async def post_brightness(request: Request):
  return Response(status_code=status.HTTP_200_OK)


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app)
