E-learning

Bu loyiha Django asosida yaratilgan va onlayn test tizimini boshqaradi.

## O'rnatish
1. Python va pip o'rnatilganligiga ishonch hosil qiling.
2. Loyiha papkasida `pip install -r requirements.txt` buyrug'ini bajaring.
3. Ma'lumotlar bazasini migratsiya qilish uchun `python manage.py migrate` buyrug'ini bajaring.
4. Default superuser teacher va student yaratish uchun `python manage.py create_users_and_permissions` buyrug'ini bajaring.
5. Djangoni ishga tushirish uchun `python manage.py runserver` buyrug'ini bajaring.


## Kodlar haqida umumiy izoh
Serializerlarni bir biriga bog'lab ishlatishdan chetlab otganman chunki realniy proektlada agar serializerlarda bir biriga 
ulanishlar bo'lsa va ma'lumotlar ko'p bolsa sayt ishlashi sekinlashadi bir birga bog'liq bo'lgan ma'lumotlar link orqakli ?query.params 
orqali id sidan filterlanib oladi bu kodni tezroq ishlashini ta'minlab beradi va ma'lumotlarni olishda prefetch_related funksiyasi ishlatilgan bundan asosiy maqsad ma'lumotlarni
bir martda so'rov kelganini ozida hamma bog'liqliklarni ovolish uchun. 


Kodlar haqidagi to'lliq tushunchani zoom orqali izohlab beraman bundan tashqari apilarni korish va ishlatish uchun postmanda api tayyor postman ni 
korishilar uchun manga email yuborsela qoshib qoyaman postmanga.

