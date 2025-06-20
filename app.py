from quart import Quart, Blueprint
from quart_cors import cors

app = Quart(__name__)
app = cors(app)


@app.route("/")
async def hello():
    return "Hello from Blueprint!"


if __name__ == '__main__':
    app.run()
