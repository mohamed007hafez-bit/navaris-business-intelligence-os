# NAVARIS - Business Intelligence OS
# الكود الواحد اللي بيخلص كل حاجة

import os

def make_agent_file():
    text = """# NAVARIS AGENT
انت NAVARIS - مساعد محمد حافظ
مهمتك: SCAN -> REVIEW -> ADD -> IMPROVE
1. SCAN: اقرا كل الملفات
2. REVIEW: راجع الارقام
3. ADD: ضيف اللي ناقص
4. IMPROVE: حسن التقرير
ممنوع تبعت لاي عميل من غير Yes من محمد
"""
    with open("NAVARIS-AGENT.md", "w", encoding="utf-8") as f:
        f.write(text)
    print("✅ 1 - عملت NAVARIS-AGENT.md")

def make_message_file():
    text = """رسالة للشركات:
السلام عليكم - انا محمد حافظ - NAVARIS
نقدر نساعدكم في Supply Vessel - Maintenance - X-Ray للمشاريع
تحب ابعتلكم عرض سريع؟
"""
    with open("MESSAGE-COMPANIES.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("✅ 2 - عملت MESSAGE-COMPANIES.txt")

def calculator():
    print("\n--- حاسبة NAVARIS ---")
    try:
        days = float(input("عدد الايام : ") or 14)
        day_rate = float(input("Day Rate بالدولار : ") or 12000)
    except:
        days = 14
        day_rate = 12000
    revenue = days * day_rate
    cost = revenue * 0.65
    profit = revenue - cost
    roi = (profit / cost * 100) if cost else 0
    print(f"Revenue : ${revenue:,.0f}")
    print(f"Profit : ${profit:,.0f}")
    print(f"ROI : {roi:.1f}%")
    print("✅ 3 - الحاسبة شغالة")

def radar():
    print("\n📡 NAVARIS - RADAR شغال...")
    print("1 - مناقصات بترول")
    print("2 - شركات Supply Vessel")
    print("3 - الاتنين مع بعض")
    choice = input("اختار 1 / 2 / 3 : ")
    print(f"اخترت : {choice} - يعني الاتنين مع بعض")

    tender = input("اسم المناقصة / الشركة : ")
    vessel = input("نوع الـ Vessel المطلوب : ")
    try:
        days = float(input("عدد الايام : ") or 14)
        day_rate = float(input("Day Rate بالدولار : ") or 12000)
    except:
        days = 14
        day_rate = 12000
    deadline = input("آخر معاد للتقديم : ")

    revenue = days * day_rate
    cost = revenue * 0.65
    profit = revenue - cost
    roi = (profit / cost * 100) if cost else 0

    print(f"\n✅ RADAR لقى : {tender}")
    print(f"Vessel : {vessel}")
    print(f"آخر معاد : {deadline}")
    print(f"Revenue : ${revenue:,.0f}")
    print(f"Profit : ${profit:,.0f}")
    print(f"ROI : {roi:.1f}%")
    print("تحب أجهز X-Ray كامل ليها؟ اكتب Yes")

    with open("RADAR-REPORT.txt", "w", encoding="utf-8") as f:
        f.write(f"RADAR REPORT - {tender}\nVessel: {vessel}\nDeadline: {deadline}\nRevenue: ${revenue:,.0f}\nProfit: ${profit:,.0f}\nROI: {roi:.1f}%\n")
    print("✅ اتحفظ في RADAR-REPORT.txt")

if __name__ == "__main__":
    make_agent_file()
    make_message_file()
    calculator()
    print("\nDONE - كله تمام")
    print("اكتب رادار عشان تشغل الرادار - او Enter عشان تخرج")
    cmd = input("اكتب هنا : ").strip()
    if cmd == "رادار" or cmd.lower() == "radar":
        radar()
    print("خلصت - اقفل وامشي")
