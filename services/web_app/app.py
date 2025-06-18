# Script to use to launch the application
import os
import sys

sys.path.append(os.path.dirname(__file__))
from app_factory import AppFactory

factory = AppFactory()
app = factory.create_app()
