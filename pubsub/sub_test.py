from flask import Flask, request
import json
import base64

app = Flask(__name__)

@app.route("/", methods=["POST"])
def receive_sub():
    envelope = json.loads(request.data.decode('utf-8'))
    msg_data = envelope["message"]["data"]

    payload = base64.b64decode(msg_data)
    print(envelope)
    
    with open("/home/ubuntu/sample.wav", "wb") as f:
        f.write(payload)
    
    return "OK", 200

if __name__ == "__main__":
    app.run(port=8080, debug=True)
