# import fastapi 
# import pydantic_models
# from fastapi import FastAPI, Query,Path, File, UploadFile
# api = fastapi.FastAPI()
# fake_database = {'users':[
#  {
#  "id":1,
#  "name":"Anna",
#  "nick":"Anny",
#  "balance": 15300
#  },
#  {
#  "id":2,
#  "name":"Dima",
#  "nick":"dimon",
#  "balance": 160.23
#  },
#  {
#  "id":3,
#  "name":"Vladimir",
#  "nick":"Vova",
#  "balance": 200.1
#  }
#  ], }
# @api.get("/items/")
# def read_items(q: str | None = Query(default=None, max_length=50)):
#  results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#  if q:
#     results.update({"q": q})
#  return results

# @api.get("/item/{item_id}")
# def read_items(
#  *,
#  item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
#  q: str,
# ):
#  results = {"item_id": item_id}
#  if q:
#     results.update({"q": q})
#  return results

# @api.put('/user/{user_id}')
# def update_user(user_id: int, user: pydantic_models.User = fastapi.Body()):
#  for index, u in enumerate(fake_database['users']):
#     if u['id'] == user_id:
#         fake_database['users'][index] = user
#  return user

# # @api.get('/responce_test')
# # def responce_test():
# #  return fastapi.Response('Hello', status_code=200,media_type='application/json')

# @api.post("/files/")
# async def create_file(file: bytes = File()):
#  return {"file_size": len(file)} # вернет клиенту размер полученного файла
# @api.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#  return {"filename": file.filename} # вернет клиенту имя полученного файла
import fastapi
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
api = fastapi.FastAPI()
html = """
<!DOCTYPE html>
<html>
 <head>
 <title>Chat</title>
 </head>
 <body>
 <h1>WebSocket Chat</h1>
 <form action="" onsubmit="sendMessage(event)">
 <input type="text" id="messageText" autocomplete="off"/>
 <button>Send</button>
 </form>
 <ul id='messages'>
 </ul>
 <script>
 var ws = new WebSocket("ws://localhost:8000/ws");
 ws.onmessage = function(event) {
 var messages = document.getElementById('messages')
 var message = document.createElement('li')
 var content = document.createTextNode(event.data)
 message.appendChild(content)
 messages.appendChild(message)
 };
 function sendMessage(event) {
 var input = document.getElementById("messageText")
 ws.send(input.value)
 input.value = ''
 event.preventDefault()
 }
 </script>
 </body>
</html>
"""
@api.get("/")
async def get():
 return HTMLResponse(html)
@api.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
 await websocket.accept()
 while True:
    data = await websocket.receive_text()
    await websocket.send_text(f"Message text was: {data}")