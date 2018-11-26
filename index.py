from sanic import Sanic
from sanic.response import json
from find_tickets import find_tickets
import cv2

app = Sanic()

@app.route("/")
async def test(request):
    example = cv2.imread('test.jpg')
    tickets = find_tickets(example)
    return json(tickets)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
