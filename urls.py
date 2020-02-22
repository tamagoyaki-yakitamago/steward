import responder

api = responder.API()


@api.route("/")
class Index:
    def on_get(self, req, res):
        res.headers["Content-Type"] = "text/html; charset=utf-8"

        res.content = api.template("index.html")