import azure.functions as func
import logging

# Import the Flask app from first.py
from first import app as flask_app

# Wrap the Flask app with WsgiFunctionApp
app = func.WsgiFunctionApp(app=flask_app.wsgi_app, http_auth_level=func.AuthLevel.ANONYMOUS)
