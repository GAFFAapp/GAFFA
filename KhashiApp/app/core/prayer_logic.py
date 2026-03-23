import requests
from datetime import datetime

class PrayerEngine:
    def __init__(self, city="Tangier", country="Morocco"):
        self.city = city
        self.country = country
        self.base_url = "http://api.aladhan.com/v1/timingsByCity"

    def get_times(self):
        params = {
            'city': self.city,
            'country': self.country,
            'method': 3  # تقويم رابطة العالم الإسلامي
        }
        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                data = response.json()['data']
                return {
                    'timings': data['timings'],
                    'date': data['date']['readable'],
                    'hijri': data['date']['hijri']['date']
                }
            return None
        except Exception as e:
            print(f"Error in Lab Engine: {e}")
            return None

    def get_next_prayer(self, timings):
        now = datetime.now().strftime("%H:%M")
        # منطق بسيط للمختبر لتحديد الصلاة القادمة
        prayers = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
        for p in prayers:
            if timings[p] > now:
                return {"name": p, "time": timings[p]}
        return {"name": "Fajr", "time": timings['Fajr']} # صلاة الفجر لليوم التالي

