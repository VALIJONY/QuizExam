<div align="center">

# ExamPlatform

**Davlat imtihonlariga tayyorgarlik tizimi**
Fanlar boʻyicha test savollari: darhol javobni koʻrsatadigan **oʻrganish rejimi** va 30 daqiqalik **imtihon rejimi**.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3-06B6D4?logo=tailwindcss&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![Savollar](https://img.shields.io/badge/savollar-863-2563eb)
![Fanlar](https://img.shields.io/badge/fanlar-7-2563eb)

<img src="docs/screenshots/exam-mode.webp" alt="Imtihon rejimi" width="100%">

</div>

---

## Mundarija

- [Nima qiladi](#nima-qiladi)
- [Skrinshotlar](#skrinshotlar)
- [Imkoniyatlar](#imkoniyatlar)
- [Texnologiyalar](#texnologiyalar)
- [Qanday ishlaydi](#qanday-ishlaydi)
- [Tez boshlash](#tez-boshlash)
- [Savollarni yuklash](#savollarni-yuklash)
- [Loyiha tuzilishi](#loyiha-tuzilishi)
- [Rivojlantirish rejasi](#rivojlantirish-rejasi)

---

## Nima qiladi

Talaba roʻyxatdan oʻtadi, fanni tanlaydi va ikki usulda tayyorlanadi:

- **Oʻrganish** — fandagi barcha savollar; variant bosilishi bilan toʻgʻri/notoʻgʻri javob darhol koʻrsatiladi.
- **Imtihon** — fandan **30 ta tasodifiy savol**, **30 daqiqa** taymer va progress-bar. Yakunda natija foizda va rangda chiqadi.

Administrator esa oʻz panelida fanlar va savollarni qoʻshadi, tahrirlaydi, oʻchiradi.

## Skrinshotlar

<table>
  <tr>
    <td width="50%"><img src="docs/screenshots/subjects.webp" alt="Fanlar"><br><sub><b>Fanlar</b> — har biri uchun “Oʻrganish” va “Imtihon”</sub></td>
    <td width="50%"><img src="docs/screenshots/learn-mode.webp" alt="Oʻrganish rejimi"><br><sub><b>Oʻrganish rejimi</b> — javob darhol tekshiriladi</sub></td>
  </tr>
  <tr>
    <td><img src="docs/screenshots/exam-mode.webp" alt="Imtihon rejimi"><br><sub><b>Imtihon rejimi</b> — 30 ta savol, taymer, progress-bar</sub></td>
    <td><img src="docs/screenshots/admin-dashboard.webp" alt="Admin panel"><br><sub><b>Admin panel</b> — statistika va savollar boshqaruvi</sub></td>
  </tr>
</table>

## Imkoniyatlar

**Talaba uchun**
- Roʻyxatdan oʻtish, kirish, chiqish
- Fanlar roʻyxati; har bir fan uchun ikki rejim
- **Oʻrganish rejimi:** variant tanlanganda sahifa yangilanmasdan (`fetch` → JSON) toʻgʻri javob tekshiriladi
- **Imtihon rejimi:** `ORDER BY RANDOM()` bilan har safar boshqa 30 ta savol; 30:00 taymer, javob berilgan savollar ulushini koʻrsatadigan progress-bar; topshirishdan oldin tasdiq soʻraladi, vaqt tugaganda topshirish oynasi ochiladi
- Natija sahifasi: toʻgʻri javoblar soni va foiz (≥70% yashil, ≥50% sariq, undan past qizil)

**Administrator uchun** (`is_superuser`)
- Dashboard: fanlar, savollar va talabalar soni, soʻnggi savollar
- Savollar va fanlar boʻyicha toʻliq **CRUD**, sahifalangan roʻyxatlar (20 tadan)
- Django admin: fan boʻyicha filtr, matn boʻyicha qidiruv, imtihon natijalari

## Texnologiyalar

| Nima | Vazifasi |
| --- | --- |
| **Django 6** — class-based view'lar | Marshrutlash, ORM, autentifikatsiya, admin |
| **Django Templates** | Server tomonida render qilingan sahifalar |
| **Tailwind CSS** (CDN) + `static/css/quiz.css` | Interfeys |
| **Vanilla JS** — sahifadagi skriptlar va [`static/js/quiz.js`](static/js/quiz.js) | Taymer, progress-bar, javobni tekshirish (`fetch`) |
| **SQLite** | Baza (qoʻshimcha oʻrnatish shart emas) |
| `django-cors-headers` | CORS |

## Qanday ishlaydi

```mermaid
flowchart LR
    T[Talaba] --> H[Fanlar]
    H --> L[Oʻrganish rejimi]
    H --> E[Imtihon rejimi]
    L -->|POST /api/check-answer/id| C{{CheckAnswerView}}
    C -->|is_correct, correct_answer| L
    E -->|30 tasodifiy savol| F[Forma + 30:00 taymer]
    F -->|POST javoblar| S[Ball hisoblanadi]
    S --> R[(ExamResult)]
    R --> P[Natija sahifasi]
```

```mermaid
erDiagram
    Subject ||--o{ Question : "savollar"
    Subject ||--o{ ExamResult : "natijalar"
    User ||--o{ ExamResult : "talaba"

    Question {
        text text
        string option_a
        string option_b
        string option_c
        string option_d
        char correct_answer "A | B | C | D"
    }
    ExamResult {
        int score
        int total_questions
        datetime date_taken
    }
```

## Tez boshlash

Talab: **Python 3.12+**.

```bash
# 1. Muhit va bogʻliqliklar
python -m venv venv
source venv/bin/activate              # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Baza va savollar (7 ta fan, 863 ta savol)
python manage.py migrate
python manage.py loaddata questions

# 3. Administrator
python manage.py createsuperuser

# 4. Ishga tushirish
python manage.py runserver
```

Sayt: <http://127.0.0.1:8000> · Admin panel: <http://127.0.0.1:8000/admin/> · Boshqaruv paneli: <http://127.0.0.1:8000/dashboard/>

> Tailwind va Inter shrifti CDN orqali yuklanadi, shuning uchun sahifalar toʻliq koʻrinishi uchun internet kerak.

## Savollarni yuklash

Yangi savollarni uch usulda qoʻshish mumkin:

1. **Admin panel** — `/dashboard/questions/add/` orqali bittalab.
2. **JSON** — [`importdata.py`](importdata.py) (`datajt*.json` → baza). Har bir element:

   ```json
   {
     "subject_id": 8,
     "text": "Savol matni",
     "option_a": "…", "option_b": "…", "option_c": "…", "option_d": "…",
     "correct_answer": "D"
   }
   ```

3. **Oddiy matn** — [`import_text.py`](import_text.py) (`text.txt` → baza). Savollar `+++++` bilan, variantlar `====` bilan ajratiladi, toʻgʻri variant boshiga `#` qoʻyiladi:

   ```text
   1. Texnologiya tushunchasi
    ====
    #biron-bir ishda qoʻllaniladigan uslublar toʻplami
    ====
    tiklash, toʻldirish
    ====
    …
    ====
    …
    +++++
   ```

Ikkala skript ham takroriy savollarni qayta yozmaydi. Fan raqami va fayl nomi skript ichida belgilangan — kerakli fanga moslab oʻzgartiring, keyin `python importdata.py` yoki `python import_text.py`.

## Loyiha tuzilishi

```text
QuizExam/
├── config/                 # settings, urls, wsgi/asgi
├── quiz/
│   ├── models.py           # Subject, Question, ExamResult
│   ├── views.py            # talaba va admin view'lari
│   ├── urls.py  admin.py
│   ├── templatetags/       # mul, div filtrlari (foiz hisobi)
│   └── fixtures/questions.json   # 7 fan, 863 savol
├── templates/              # base, home, login, register, dashboard, CRUD formalari
│   └── quiz/               # learn, exam, result
├── static/                 # css/quiz.css, js/quiz.js
├── importdata.py  import_text.py   # savollarni yuklash skriptlari
├── data1.json  data3.json  data4.json  datajt*.json  text.txt   # savollar manbalari
└── docs/screenshots/
```

## Rivojlantirish rejasi

- [ ] Sozlamalarni muhit oʻzgaruvchilariga koʻchirish (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, CORS) — hozir `config/settings.py` da dasturlash qiymatlari
- [ ] Talabaning barcha urinishlari tarixi va xatolar ustida ishlash (imtihondan keyin javoblarni koʻrib chiqish)
- [ ] Imtihon savollari sonini fan boʻyicha sozlash (hozir 30 ta)
- [ ] Avtomatik testlar (`quiz/tests.py`)
- [ ] `import_*` skriptlarini `manage.py` buyruqlariga aylantirish
