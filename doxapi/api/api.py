from flask_restplus import Api

from doxapi.app import app


api = Api(
    app,
    doc="/api",
    prefix="/api",
    version="0.1",
    title="Documents API",
    security="apikey",
    authorizations={
        "apikey": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
)
