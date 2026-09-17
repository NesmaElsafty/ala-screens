# -*- coding: utf-8 -*-
import json
import os

p = os.path.join(os.path.dirname(__file__), "ar.json")
d = json.load(open(p, encoding="utf-8"))
extra = {
    "Language": "اللغة",
    "English": "English",
    "Close menu": "أغلق القائمة",
    "UPCOMING EVENTS": "الفعاليات القادمة",
    "LATEST NEWS": "آخر الأخبار",
    "Revenue Growth": "نمو الإيرادات",
    "Customer Growth": "نمو العملاء",
    "Kids": "للأطفال",
    "Hotel": "فندق",
    "Limited": "محدود",
    "Desert": "الصحراء",
    "Camp Atmosphere & Guidelines": "أجواء المعسكر والإرشادات",
    "Maadi, Cairo — Egypt": "المعادي، القاهرة — مصر",
    "— Find the learning experience that best fits your goals.": " — اعثر على التجربة التعليمية الأنسب لأهدافك.",
    "— Get the latest verified schedule, pricing, and available offers.": " — احصل على أحدث المواعيد المعتمدة والأسعار والعروض المتاحة.",
    "— Our team will help you complete your registration with ease.": " — سيساعدك فريقنا على إتمام تسجيلك بسهولة.",
    "— Dr. Ahmed Latif Mohamed Hassan, CEO, Ahmed Latif Academy (ALA) for Training and Consultancies": " — د. أحمد لطيف محمد حسن، الرئيس التنفيذي، Ahmed Latif Academy (ALA) للتدريب والاستشارات",
    "ICF-PCC": "ICF-PCC",
    "PhD + MBA": "PhD + MBA",
    "Dynamo": "Dynamo",
    "PCC": "PCC",
    "120K LE": "120 ألف جنيه",
    "33M LE": "33 مليون جنيه",
    "600k+": "600 ألف+",
    "You're just one step away from joining ALA! Contact us today, and one of our team members will be happy to assist you with the next available course date, course fees, current offers, answer all your questions, and help you complete your registration with ease.": "أنت على بُعد خطوة واحدة من الانضمام إلى ALA! تواصل معنا اليوم، وسيسعد أحد أعضاء فريقنا بمساعدتك بموعد الدورة المتاح التالي، والرسوم، والعروض الحالية، والإجابة عن كل أسئلتك، وإتمام تسجيلك بسهولة.",
    "Hello ALA, I'm interested in: ": "مرحباً ALA، أنا مهتم/ة بـ: ",
    "Name: ": "الاسم: ",
    "Phone: ": "الهاتف: ",
    "Email: ": "البريد: ",
    "Message: ": "الرسالة: ",
    "Please share the next available course date, fees, and current offers.": "يرجى مشاركة أقرب موعد متاح للدورة والرسوم والعروض الحالية.",
}
n = 0
for k, v in extra.items():
    if k not in d:
        d[k] = v
        n += 1
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("added", n, "total", len(d))
