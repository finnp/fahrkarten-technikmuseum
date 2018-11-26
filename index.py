from sanic import Sanic
from sanic.response import json, text
from find_tickets import find_tickets
import cv2
import numpy as np

app = Sanic()

@app.route("/")
async def test(request):
    return text("Usage: curl -X POST <server>/findtickets -F 'data=@test.jpg'. Returns a list of found tickets")

@app.route("findtickets", methods=['POST'])
async def ticket(request):
    img_str = request.files['data'][0].body
    arr = np.frombuffer(img_str, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    tickets = find_tickets(img)
    return json(tickets)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
