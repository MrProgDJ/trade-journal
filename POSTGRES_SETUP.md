# اضافه کردن PostgreSQL به پروژه Railway

## مراحل:

1. **در داشبورد Railway پروژه `trade-journal-production`:**
   - کلیک کن **+ New** → **Database** → **PostgreSQL**
   - صبر کن تا ساخته بشه

2. **متغیر `DATABASE_URL` به صورت خودکار به سرویس Django اضافه میشه**
   - برو سرویس اصلی (Django) → **Variables** → باید `DATABASE_URL` رو ببینی

3. **Redeploy کن** — همین!

**چیزایی که تغییر کرد:**
- `settings.py` از `dj_database_url` استفاده میکنه → اگه `DATABASE_URL` باشه PostgreSQL، وگرنه SQLite
- `requirements.txt` حالا `psycopg2-binary` و `dj-database-url` داره
- بعد از redeploy، superuser خودکار ساخته میشه با همون `admin/admin123`

**⚠️ مهم:** دیتاهای قبلی (معاملاتی که ثبت کردی) پاک میشن چون روی SQLite بودن و به PostgreSQL جدید منتقل نمیشن. اگه دیتا داری بهم بگو تا backup/restore اضافه کنم.
