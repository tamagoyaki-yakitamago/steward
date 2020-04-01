import responder

from process import add_headers, select_random, get_max_value, set_session, check_session
api = responder.API()


@api.route("/")
class Index:
    # GET method
    def on_get(self, req, res):
        add_headers(res)
        set_session(res)
        csrf_token = res.session["token"]
        
        res.content = api.template("index.html", csrf_token=csrf_token)

    # POST method
    async def on_post(self, req, res):
        add_headers(res)
        data = await req.media()
        name_dict = {}
        name_list = []
        message = ""
        error_message = ""

        if len(data) - 1 < 2 or 100 < len(data) - 1:
            error_message = "人数は2人から100人の間になります。"
        elif not check_session(res, data.get("_csrf_token")):
            error_message = "技術的な問題が発生しました、時間をおいて再度やり直してください。"
        else:
            for i in range(len(data) - 1):
                name = data.get(f"entryname[{i}]")
                name_list.append(name)
                name_dict[name] = 0

            while True:
                name_dict = select_random(name_list, name_dict)

                max_name, count = get_max_value(name_list, name_dict)
                if count == 0:
                    break

            message = max_name

        set_session(res)
        csrf_token = res.session["token"]
        
        res.content = api.template("index.html", message=message, error_message=error_message, csrf_token=csrf_token)
