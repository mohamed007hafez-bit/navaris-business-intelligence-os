# NAVARIS - ONE CODE - محمد حافظ - يخلص كل حاجة مرة واحدة
# شغل الكود ده بالأمر ده: python navaris.py

import os

print("=== NAVARIS - بدأ الشغل - محمد حافظ ===")

# 1 - انشاء المحرك الأساسي - Autonomous Agent
agent = """# NAVARIS AUTONOMOUS AGENT - المحرك الأساسي - محمد حافظ
YOU ARE NAVARIS AGENT - Autonomous - Like Meta AI
JOB: SCAN -> REVIEW -> ADD -> IMPROVE
RULES: NEVER use Internet - NEVER invent numbers - If DATA MISSING write: DATA MISSING - اسأل محمد حافظ
BRAND: محمد حافظ ONLY - NOT HAFEZROCK
MONEY: 100,000 EGP = 2,061 USD - Show EGP + USD + SAR + EUR
30% / 70%: Client sees 30% ONLY - 70% Locked - تواصل مع محمد حافظ
HUMAN GATE: Mohamed Hafez = YES - قبل ما تبعت لأي عميل
Accept 5 clients / month ONLY - 50% Advance - Bank Only
"""

with open("NAVARIS-AGENT.md", "w", encoding="utf-8") as f:
    f.write(agent)
print("✅ 1 - عملت NAVARIS-AGENT.md - المحرك الأساسي")

# 2 - انشاء ملف الرسالة للشركات
msg = """السلام عليكم - أنا محمد حافظ - Mohamed Hafez - NAVARIS
بساعد شركات البترول والطاقة والنقل الدولي واللوجستيات والتوكيلات الملاحية
في 15 دقيقة - بعمل Business X-Ray - أشعة مجانية 30%
1. هتكسب كام؟ ROI - Payback - Break-even
2. فين الخطر الواحد اللي بيخسرك فلوس؟
3. ايه أول 3 خطوات عشان توقف الخسارة؟
نقبل 5 شركات في الشهر فقط.
تحب نبدأ بـ 15 دقيقة امتى؟ - محمد حافظ - WhatsApp +20 1278166680
"""

with open("MESSAGE-COMPANIES.txt", "w", encoding="utf-8") as f:
    f.write(msg)
print("✅ 2 - عملت MESSAGE-COMPANIES.txt - رسالة الشركات")

# 3 - حاسبة NAVARIS - تحسب ROI - Payback - Break-even
def navaris_calc(cost, gain, fixed, price, variable):
    roi = (gain - cost) / cost * 100 if cost else 0
    payback = cost / (gain/3) if gain else 0
    breakeven = fixed / (price - variable) if price != variable else 0
    usd = cost / 48.5
    print(f"\n--- NAVARIS X-RAY ---")
    print(f"التكلفة: {cost} جنيه = {usd:.0f} دولار")
    print(f"ROI: {roi:.1f}%")
    print(f"Payback: {payback:.1f} سنة")
    print(f"Break-even: {breakeven:.0f} وحدة")
    print(f"🔒 التفاصيل الكاملة 70% - تواصل مع محمد حافظ")
    return roi

# مثال: مصنع أغذية - 100,000 جنيه
navaris_calc(cost=100000, gain=150000, fixed=30000, price=100, variable=60)

print("\n✅ 3 - الحاسبة شغالة - جرب تغير الأرقام")
print("\n=== NAVARIS - خلص كل حاجة - DONE ===")
print("اللي بعد كده: ارفع الملفين دول على GitHub - Add file - Upload")