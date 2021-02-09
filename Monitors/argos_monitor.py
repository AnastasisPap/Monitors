import requests
from bs4 import BeautifulSoup
from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
from datetime import datetime
import os


def get_time():
    return datetime.now().strftime("%H:%M:%S")
