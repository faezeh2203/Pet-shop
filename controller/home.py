from flask import Flask, render_template
import requests
from app import app

class Home:

    def __init__(self, *args, **kwargs):
        pass
    
    def main(self):
        # ارسال درخواست به API برای دریافت لیست نژادها
        response = requests.get("https://dog.ceo/api/breeds/list/all")
        if response.status_code == 200:
            breed_data = response.json()  # دریافت داده‌ها از API
            breeds = breed_data['message']  # استخراج نژادها از پیام

            # افزودن لینک تصویر برای هر نژاد
            breed_images = {}
            for breed in breeds:
                image_response = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random")
                if image_response.status_code == 200:
                    breed_images[breed] = image_response.json()['message']
                else:
                    breed_images[breed] = None
        else:
            breeds = {}
            breed_images = {}

        return render_template('home.html', breeds=breeds, breed_images=breed_images)
