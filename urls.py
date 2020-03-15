import responder

api = responder.API()


@api.route("/")
class Index:
    # Add headers
    def add_headers(self, res):
        res.headers["Content-Type"] = "text/html; charset=utf-8"

    # GET method
    def on_get(self, req, res):
        self.add_headers(res)

        res.content = api.template("index.html")

    # POST method
    async def on_post(self, req, res):
        self.add_headers(res)
        data = await req.media()
        
        for i in range(len(data)):
            print(data.get(f"entryname[{i}]"))

        res.content = api.template("index.html")
