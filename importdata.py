# import_data.py
import os
import json
import django

# 1. Django muhitini tashqaridan turib ishga tushirish
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Muhit tayyor bo'lgach, modellarni chaqiramiz
from quiz.models import Question, Subject

def import_questions():
    # 2. Bazada "Subject" (Fan) bor-yo'qligini tekshiramiz. Yo'q bo'lsa, avtomatik yaratamiz.
    # JSON dagi subject_id: 1 aynan shu fanga bog'lanadi.
    subject, created = Subject.objects.get_or_create(
        id=4,
        defaults={
            'name': "Ona tili va o'qish savodxonligi", 
            'description': "Boshlang'ich sinf ta'lim metodikasi bo'yicha testlar"
        }
    )
    if created:
        print(f"Bazada yangi fan yaratildi: {subject.name}")

    # 3. JSON faylni o'qish
    try:
        with open('data4.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("XATOLIK: 'data4.json' fayli topilmadi!")
        return

    # 4. Savollarni bazaga yozish
    count = 0
    for item in data:
        # Xavfsizlik uchun: agar xuddi shu savol bazada bo'lsa, uni qayta yozmaymiz
        if not Question.objects.filter(text=item['text'], subject=subject).exists():
            Question.objects.create(
                subject=subject,
                text=item['text'],
                option_a=item['option_a'],
                option_b=item['option_b'],
                option_c=item['option_c'],
                option_d=item['option_d'],
                correct_answer=item['correct_answer']
            )
            count += 1

    print(f"✅ Muvaffaqiyatli: Bazaga {count} ta yangi savol yozildi!")

if __name__ == '__main__':
    print("Savollarni bazaga yuklash boshlandi...")
    import_questions()