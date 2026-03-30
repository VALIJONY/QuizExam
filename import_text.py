# import_text.py
import os
import re
import django

# Django muhitini ulash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from quiz.models import Question, Subject

def import_raw_text():
    # 2-fan (Texnologiya) bazada bo'lmasa yaratamiz
    subject, _ = Subject.objects.get_or_create(
        id=2,
        defaults={
            'name': 'Texnologiya va uni o‘qitish metodikasi',
            'description': 'Texnologiya fani bo‘yicha barcha test savollari'
        }
    )

    try:
        with open('text.txt', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("XATOLIK: 'text.txt' fayli topilmadi!")
        return

    # Savollarni "+++++" belgisi orqali ajratib olamiz
    blocks = content.split('+++++')
    count = 0

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Har bir savol va javobni "====" orqali ajratamiz
        parts = block.split('====')
        parts = [p.strip() for p in parts if p.strip()]

        if len(parts) == 5:
            q_text = parts[0]
            opts = parts[1:5]
        elif len(parts) == 4:
            # Ba'zi savollarda "====" qolib ketgan bo'lsa, xatoni to'g'irlaymiz
            lines = parts[0].split('\n', 1)
            if len(lines) > 1:
                q_text = lines[0].strip()
                opts = [lines[1].strip()] + parts[1:4]
            else:
                continue
        else:
            continue

        # Savol boshidagi "1. ", "2. " kabi raqamlarni tozalab tashlaymiz
        q_text = re.sub(r'^\d+\.\s*', '', q_text)

        options_dict = {}
        correct_ans = 'A'
        letters = ['A', 'B', 'C', 'D']

        # To'g'ri javobni "#" belgisi orqali topamiz
        for i, opt in enumerate(opts):
            if opt.startswith('#'):
                correct_ans = letters[i]
                opt = opt[1:].strip()
            options_dict[letters[i]] = opt

        # Dublikat bo'lmasa bazaga yozamiz
        if not Question.objects.filter(text=q_text, subject=subject).exists():
            Question.objects.create(
                subject=subject,
                text=q_text,
                option_a=options_dict['A'],
                option_b=options_dict['B'],
                option_c=options_dict['C'],
                option_d=options_dict['D'],
                correct_answer=correct_ans
            )
            count += 1

    print(f"✅ Ajoyib! Bazaga {count} ta yangi savol muvaffaqiyatli yuklandi!")

if __name__ == '__main__':
    print("Savollarni tahlil qilish va bazaga yozish boshlandi...")
    import_raw_text()