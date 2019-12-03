from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS

from server.routes.authentication import authentication_api
from server.routes.projects import projects_api
from server.routes.resources import resources_api
from server.routes.plugins import plugins_api
from server.routes.tags import tags_api
from server.routes.apikeys import apikeys_api

# Workaround due to template confusion between jinja2 and Vue
# See: https://github.com/yymm/flask-vuejs
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(
        dict(
            block_start_string="(%",
            block_end_string="%)",
            variable_start_string="((",
            variable_end_string="))",
            comment_start_string="(#",
            comment_end_string="#)",
        )
    )


app = CustomFlask(__name__)
app.register_blueprint(authentication_api)
app.register_blueprint(projects_api)
app.register_blueprint(resources_api)
app.register_blueprint(plugins_api)
app.register_blueprint(tags_api)
app.register_blueprint(apikeys_api)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api_app = Api(app)

if __name__ == "__main__":
    # TODO: Remove debug param in production
    app.run(debug=True)
