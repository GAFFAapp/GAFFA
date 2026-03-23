import time
import os

# مصفوفة اليقين (Data Array)
reminders = [
    "يا إسماعيل: الصلاة هي نظام تبريد الروح.. أطفئ نيران التشتت.",
    "تذكر الخوارزمي: أي مشكلة معقدة هي مجرد خطوات بسيطة متسلسلة.",
    "فيزياء اليقين: الكون لا يتحرك بالصدفة، بل بنظام 'Success' محكم.",
    "الخالق لديه Root Access: لا تقلق من المستقبل، المصدر معك."
]

def clear_terminal():
    os.system('clear')

def start_focus_mode():
    index = 0
    while True:
        clear_terminal()
        print("="*40)
        print("   GAFFA ISMAIL - SYSTEM STABILITY   ")
        print("="*40)
        print(f"\n[!] {reminders[index % len(reminders)]}\n")
        print("="*40)
        
        index += 1
        # انتظر 10 ثواني (أو غيرها كما تحب) قبل التذكير القادم
        time.sleep(10)

if __name__ == "__main__":
    try:
        start_focus_mode()
    except KeyboardInterrupt:
        print("\n[+] تم إيقاف التذكير.. عد لعملك بيقين وتركيز.")

