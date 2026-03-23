from flask import Flask, render_template, jsonify
from app.core.prayer_logic import PrayerEngine

app = Flask(__name__, 
            template_folder='app/templates', 
            static_folder='app/static')

engine = PrayerEngine()

@app.route('/')
def index():
    data = engine.get_times()
    next_p = engine.get_next_prayer(data['timings'])
    return render_template('index.html', prayer_data=data, next_prayer=next_p)

@app.route('/api/status')
def status():
    # API داخلي للتحديث اللحظي بدون إعادة تحميل الصفحة
    data = engine.get_times()
    return jsonify(data)

if __name__ == '__main__':
    # تشغيل الخادم في وضع التطوير (Debug Mode)
    app.run(debug=True, port=5000)

