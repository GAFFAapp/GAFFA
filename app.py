from flask import Flask, render_template_string, request
from collections import Counter
from textblob import TextBlob
import re

app = Flask(__name__)

def analyze_all(raw_text):
    posts = [p.strip() for p in raw_text.split('\n') if p.strip()]
    if not posts: return None
    
    # 1. تحليل التكرار
    cleaned = [re.sub(r'[^\w\s]', '', p.lower()) for p in posts]
    dup_check = Counter(cleaned)
    dup_count = sum(c for m, c in dup_check.items() if c > 1)
    rate = (dup_count / len(posts)) * 100
    
    # 2. تحليل المشاعر
    full_blob = TextBlob(raw_text)
    score = full_blob.sentiment.polarity # من -1 إلى 1
    
    # تحويل القطبية لنسب مئوية للعرض في الرسم البياني
    pos = max(0, score) * 100
    neg = abs(min(0, score)) * 100
    neu = 100 - (pos + neg)

    return {
        "rate": round(rate, 2),
        "pos": round(pos, 2),
        "neg": round(neg, 2),
        "neu": round(neu, 2),
        "total": len(posts)
    }

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة تحكم الرصد الرقمي</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background: #1a1a1a; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; }
        .container { max-width: 800px; margin: auto; }
        textarea { width: 100%; background: #333; color: white; border: none; border-radius: 8px; padding: 10px; margin-bottom: 10px; }
        .btn { background: #007bff; color: white; border: none; padding: 10px 25px; border-radius: 5px; cursor: pointer; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; }
        .card { background: #252525; padding: 20px; border-radius: 12px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ مرصد التضليل الرقمي</h1>
        <form method="post">
            <textarea name="content" rows="6" placeholder="الصق المنشورات هنا للتحليل..."></textarea>
            <button class="btn" type="submit">بدء التحليل</button>
        </form>

        {% if res %}
        <div class="grid">
            <div class="card">
                <h3>مؤشر التنسيق (البوتات)</h3>
                <h1 style="color: #ff4757;">{{ res.rate }}%</h1>
                <p>نسبة التكرار المتطابق</p>
            </div>
            <div class="card">
                <canvas id="sentimentChart"></canvas>
            </div>
        </div>

        <script>
            const ctx = document.getElementById('sentimentChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['إيجابي', 'سلبي', 'محايد'],
                    datasets: [{
                        data: [{{res.pos}}, {{res.neg}}, {{res.neu}}],
                        backgroundColor: ['#2ecc71', '#e74c3c', '#95a5a6']
                    }]
                },
                options: { plugins: { title: { display: true, text: 'نبرة الخطاب العام', color: 'white' }}}
            });
        </script>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    res = None
    if request.method == 'POST':
        res = analyze_all(request.form['content'])
    return render_template_string(HTML_TEMPLATE, res=res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

