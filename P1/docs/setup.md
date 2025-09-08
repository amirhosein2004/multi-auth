# 🚀 راه‌اندازی پروژه Learnfolio (نسخه Dockerized)

## 📦 پیش‌نیازها

قبل از اجرای پروژه، اطمینان حاصل کنید که موارد زیر روی سیستم شما نصب هستند:

- Python 3.10+ (در صورت اجرای محلی)
- Node.js (در صورت اجرای فرانت‌اند به‌صورت محلی)
- Docker و Docker Compose

---

## ⚙️ مراحل راه‌اندازی در محیط Docker (بک اند)

### 1. ایجاد فایل محیطی `.env`

یک فایل `.env` در ریشه پروژه ایجاد کنید و مقادیر مناسب را وارد نمایید. می‌توانید از فایل نمونه استفاده کنید:

```bash
cp .env.example .env
```
همچنین مطمئن شوید که فایل .env برای هر سرویسی که نیاز دارد، تنظیم شده باشد (مثل دیتابیس، بک‌اند، فرانت‌اند و...).

### 2. ساخت ایمیج‌ها و اجرای سرویس‌ها
با دستور زیر همه‌ی سرویس‌ها (PostgreSQL, Redis, Django, Celery, React و ...) اجرا می‌شوند:

```bash
docker-compose up --build
```

### 3. اجرای مهاجرت‌های پایگاه‌داده
پس از بالا آمدن کانتینرها، وارد کانتینر بک‌اند شوید:

```bash
docker-compose exec backend bash
```
سپس مهاجرت‌ها را اجرا کنید:

```bash
python manage.py migrate
```

### 4. (اختیاری) ایجاد سوپر یوزر
اگر نیاز به کاربر ادمین دارید:

```bash
python manage.py createsuperuser
```

### 5. دسترسی‌ها
- بک‌اند: [http://localhost:8000](http://localhost:8000)
- فرانت‌اند: [http://localhost:3000](http://localhost:3000)
- پنل ادمین Django: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 🧪 اجرای پروژه در محیط محلی (بدون Docker)
مناسب برای توسعه سریع بخش‌های خاص پروژه

### 🔧 Backend

**نصب پکیج‌ها:**
```bash
pip install -r requirements/base.txt
```

**تنظیم فایل .env**
فایل .env را از روی نمونه بسازید و مقادیر را تنظیم کنید.

**اجرای مهاجرت‌ها:**
```bash
python manage.py migrate
```

**اجرای سرور:**
```bash
python manage.py runserver
```

**اجرای Celery**

Worker:
```bash
celery -A backend worker --loglevel=info
```

Beat:
```bash
celery -A backend beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### 🎨 Frontend

**نصب پکیج‌ها:**
```bash
cd frontend
npm install
```

**اجرای سرور:**
```bash
npm run dev
```
