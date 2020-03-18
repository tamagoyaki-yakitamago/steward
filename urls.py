import responder
import secrets

api = responder.API()


@api.route("/")
class Index:
    # Add headers
    def add_headers(self, res):
        res.headers["Content-Type"] = "text/html; charset=utf-8"
        res.headers["X-Frame-Options"] = "SAMEORIGIN"
        res.headers["X-XSS-Protection"] = "1; mode=block"

    # Select Random
    def select_random(self, name_list, name_dict):
        for i in range(100):
            n = secrets.randbelow(len(name_dict))
            name_dict[name_list[n]] += 1

        return name_dict

    # Get max value
    def get_max_value(self, name_list, name_dict):
        max = 0
        max_name = ""
        count = 0

        for name in name_list:
            if max == 0:
                max = name_dict[name_list[0]]
                max_name = name_list[0]
            elif max == name_dict[name]:
                count += 1
            elif max < name_dict[name]:
                max = name_dict[name]
                max_name = name
                count = 0

        return max_name, count

    # Set session
    def set_session(self, res):
        res.session["token"] = secrets.token_hex()

    # Check session
    def check_session(self, res, token):
        if token == res.session.get("token"):
            return True
        else:
            return False

    # GET method
    def on_get(self, req, res):
        self.add_headers(res)
        self.set_session(res)
        csrf_token = res.session["token"]
        
        res.content = api.template("index.html", csrf_token=csrf_token)

    # POST method
    async def on_post(self, req, res):
        self.add_headers(res)
        data = await req.media()
        name_dict = {}
        name_list = []
        message = ""
        error_message = ""

        if len(data) - 1 < 2 or 100 < len(data) - 1:
            error_message = "人数は2人から100人の間になります。"
        elif not self.check_session(res, data.get("_csrf_token")):
            error_message = "技術的な問題が発生しました、時間をおいて再度やり直してください。"
        else:
            for i in range(len(data) - 1):
                name = data.get(f"entryname[{i}]")
                name_list.append(name)
                name_dict[name] = 0

            while True:
                name_dict = self.select_random(name_list, name_dict)

                max_name, count = self.get_max_value(name_list, name_dict)
                if count == 0:
                    break

            message = max_name
            print(name_dict)

        self.set_session(res)
        csrf_token = res.session["token"]
        
        res.content = api.template("index.html", message=message, error_message=error_message, csrf_token=csrf_token)
