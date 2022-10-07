from flask import Flask, render_template, jsonify, current_app

from bp_api.views import bp_api
from bp_posts.views import bp_posts

from exceptions.all_exceptions import DataSourceError

import config_loggers


def create_and_app_config(config_path):
    app = Flask(__name__)

    app.config['JSON_AS_ASCII'] = False

    app.register_blueprint(bp_posts)
    app.register_blueprint(bp_api, url_prefix='/api')
    app.config.from_pyfile(config_path)
    config_loggers.config(app)

    return app


app = create_and_app_config("config.py")


@app.errorhandler(404)
def page_error_404(error):
    return f"Такой страницы нет {error}", 404


@app.errorhandler(500)
def page_error_500(error):
    return f"На сервере произошла ошибка - {error}", 500


@app.errorhandler(DataSourceError)
def page_error_data_source_error(error):
    return f"Ошибка, сайт не смог обработать данные, проверьте файл  {error}", 500


if __name__ == "__main__":
    app.run(port=8000)
