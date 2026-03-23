import requests
from flask import Flask, render_template, request
from scipy.stats import poisson
import numpy as np

app = Flask(__name__)

# مفتاح الـ API الخاص بك من All Sports API
API_KEY = "9ab1ffd9dc50d3a0b1deb308b1d3b243184167934d88636bd56af6f7fddf20cf" # احتفظ بالمفتاح الكامل كما في صورتك

def get_team_average(team_name):
    # جلب آخر النتائج للفريق من التاريخ المحدد إلى اليوم
    url = f"https://apiv2.allsportsapi.com/football/?met=fixtures&APIkey={API_KEY}&from=2025-01-01&to=2026-03-08&teamName={team_name}"
    try:
        data = requests.get(url).json()
        goals = []
        if 'result' in data:
            for match in data['result']:
                # فصل النتيجة (مثلاً 2 - 1) وتحويلها لأرقام
                score_parts = match['event_final_result'].split(' - ')
                if match['event_home_team'].lower() == team_name.lower():
                    goals.append(int(score_parts[0]))
                else:
                    goals.append(int(score_parts[1]))
            return sum(goals) / len(goals) if goals else 1.5
    except:
        return 1.5 # قيمة افتراضية في حال حدوث خطأ
    return 1.5

def calculate_best_score(t1_exp, t2_exp):
    # مصفوفة احتمالات النتائج (بواسون)
    max_goals = 6
    probs = np.outer(poisson.pmf(range(max_goals), t1_exp), 
                     poisson.pmf(range(max_goals), t2_exp))
    best_idx = np.unravel_index(np.argmax(probs), probs.shape)
    return f"{best_idx[0]}-{best_idx[1]}", round(np.max(probs) * 100, 1)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        t1_name = request.form['team1_name']
        t2_name = request.form['team2_name']
        
        # جلب البيانات الحية تلقائياً
        t1_avg = get_team_average(t1_name)
        t2_avg = get_team_average(t2_name)
        
        score, prob = calculate_best_score(t1_avg, t2_avg)
        result = {'score': score, 'prob': prob, 't1': t1_name, 't2': t2_name}
        
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

