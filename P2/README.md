# ERP Django Project

## Requirements
- Docker
- Docker Compose

## Quick Start

1. **کپی کردن فایل env.example به .env و تنظیم مقادیر:**

```bash
cp .env.example .env
```

2. **ساخت و اجرای سرویس‌ها:**

```bash
docker-compose up --build
```

3. **اجرای دستورات مدیریت (مثلاً مهاجرت دیتابیس):**

```bash
docker-compose exec django python manage.py migrate
```

4. **ساخت ادمین:**

```bash
docker-compose exec django python manage.py createsuperuser
```

5. **دسترسی به سایت:**

- برنامه: http://localhost:8000
- ادمین: http://localhost:8000/admin

## متغیرهای محیطی

در فایل `.env`:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DB_NAME=erp_db
DB_USER=erp_user
DB_PASSWORD=erp_password
DB_HOST=db
DB_PORT=5432
```

## نکات
- برای تغییر پورت‌ها یا نام دیتابیس، مقادیر را در `docker-compose.yml` و `.env` تغییر دهید.
- برای محیط production، مقدار `DEBUG` را False قرار دهید و یک `SECRET_KEY` قوی انتخاب کنید.