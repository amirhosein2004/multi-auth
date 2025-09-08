# 🔐 سیستم احراز هویت پیشرفته

<div align="center">

**🚀 سیستم احراز هویت کامل با معماری مدرن و مقیاس‌پذیر**

*پیاده‌سازی حرفه‌ای سیستم احراز هویت با استفاده از بهترین تکنولوژی‌های روز دنیا*

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django_REST-ff1709?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com/)
[![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)](https://jwt.io/)

</div>

---

## ✨ **ویژگی‌های کلیدی سیستم**

<div align="center">
<table>
  <tr>
    <td valign="top" width="50%">
      <h4 align="center">🔐 احراز هویت پیشرفته</h4>
      <ul>
        <li>🚪 <strong>Passwordless</strong>: ورود بدون رمز با OTP موبایل</li>
        <li>🔑 <strong>Password-based</strong>: ورود با شماره موبایل و رمز عبور</li>
        <li>📱 <strong>Mobile-First</strong>: احراز هویت کامل با شماره موبایل</li>
        <li>🎯 <strong>JWT Management</strong>: مدیریت توکن‌های Access و Refresh</li>
      </ul>
    </td>
    <td valign="top" width="50%">
      <h4 align="center">🔑 مدیریت کامل رمز عبور</h4>
      <ul>
        <li>🔄 <strong>Password Reset</strong>: فرآیند کامل بازیابی رمز عبور</li>
        <li>✍️ <strong>Password Management</strong>: مدیریت کامل رمز عبور</li>
        <li>🆕 <strong>Set Initial Password</strong>: امکان تعیین رمز برای اولین بار</li>
        <li>🛡️ <strong>Secure</strong>: فرآیندهای امن و مبتنی بر توکن</li>
      </ul>
    </td>
  </tr>
</table>
</div>

---

## 🛠️ **تکنولوژی‌های استفاده شده**

<div align="center">

| 🏗️ **بخش** | 💻 **تکنولوژی** | 📝 **نقش و کاربرد** |
|:----------:|:---------------:|:------------------:|
| **Backend Framework** | Django + DRF | API قدرتمند و RESTful |
| **Database** | PostgreSQL | پایگاه داده اصلی و قابل اعتماد |
| **Cache & Session** | Redis | کش سریع و مدیریت Session |
| **Authentication** | JWT (SimpleJWT) | احراز هویت امن و Stateless |
| **Containerization** | Docker | استقرار آسان و مقیاس‌پذیر |
| **API Documentation** | OpenAPI 3.0 | مستندات خودکار API |

</div>

---

## 📋 **API Endpoints - مستندات کامل**

سیستم شامل **10 endpoint** اصلی برای مدیریت کامل احراز هویت است:

### 🔐 **Authentication APIs**

<div align="center">

| 🎯 **Endpoint** | 🔧 **Method** | 📝 **توضیحات** | 🔗 **Path** |
|:-------------:|:------------:|:-------------:|:----------:|
| **Login Send OTP** | `POST` | ارسال کد OTP به شماره موبایل برای ورود | `/api/auth/v1/login/send-otp/` |
| **Login Verify OTP** | `POST` | تایید کد OTP و ورود به سیستم | `/api/auth/v1/login/verify-otp/` |
| **Login Password** | `POST` | ورود با شماره موبایل و رمز عبور | `/api/auth/v1/login/password/` |
| **Register Send OTP** | `POST` | ارسال کد OTP به موبایل برای ثبت‌نام | `/api/auth/v1/register/send-otp/` |
| **Register Verify OTP** | `POST` | تایید کد OTP و تکمیل ثبت‌نام | `/api/auth/v1/register/verify-otp/` |

</div>

### 🔑 **Password Management APIs**

<div align="center">

| 🎯 **Endpoint** | 🔧 **Method** | 📝 **توضیحات** | 🔗 **Path** |
|:-------------:|:------------:|:-------------:|:----------:|
| **Register Set Password** | `POST` | تعیین رمز عبور پس از ثبت‌نام | `/api/auth/v1/register/set-password/` |
| **Reset Password Send OTP** | `POST` | ارسال کد OTP به موبایل برای بازیابی رمز | `/api/auth/v1/reset-password/send-otp/` |
| **Reset Password Verify OTP** | `POST` | تایید کد OTP برای بازیابی رمز | `/api/auth/v1/reset-password/verify-otp/` |
| **Reset Password Set Password** | `POST` | تعیین رمز عبور جدید پس از تایید OTP | `/api/auth/v1/reset-password/set-password/` |
| **Logout** | `POST` | خروج امن از سیستم | `/api/auth/v1/logout/` |

</div>

---

## 🚀 **راه‌اندازی سریع**

### 📋 **پیش‌نیازها**
- Docker
- Docker Compose

### ⚡ **مراحل نصب**

1. **کپی کردن فایل محیطی:**
```bash
cp .env.example .env
```

2. **ساخت و اجرای سرویس‌ها:**
```bash
docker-compose up --build
```

3. **اجرای مهاجرت دیتابیس:**
```bash
docker-compose exec django python manage.py migrate
```

4. **ساخت کاربر ادمین:**
```bash
docker-compose exec django python manage.py createsuperuser
```

5. **دسترسی به سرویس‌ها:**
- 🌐 **برنامه اصلی**: http://localhost:8000
- ⚙️ **پنل ادمین**: http://localhost:8000/admin
- 📚 **مستندات API**: http://localhost:8000/api/docs/

---

## ⚙️ **تنظیمات محیطی**

در فایل `.env` موارد زیر را تنظیم کنید:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# Database Configuration
DB_NAME=auth_db
DB_USER=auth_user
DB_PASSWORD=secure_password
DB_HOST=db
DB_PORT=5432
```

---

## 📸 **نمونه‌های عملی سیستم**

### 🖼️ **تصاویر و نتایج احراز هویت**

<div align="center">


### 📱 **تصاویر فرآیند کامل احراز هویت **

<div align="center" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; align-items: center;">

![picture1](./docs/assets/Screenshot%202025-09-08%20111641.png)
![picture2](./docs/assets/Screenshot%202025-09-08%20111659.png)

![picture3](./docs/assets/Screenshot%202025-09-08%20111714.png)
![picture4](./docs/assets/Screenshot%202025-09-08%20111729.png)

![picture5](./docs/assets/Screenshot%202025-09-08%20111810.png)

</div>

</div>

---

## 🔧 **نکات فنی و بهینه‌سازی**

### 🚀 **عملکرد**
- استفاده از Redis برای کش کردن OTP ها
- پیاده‌سازی Rate Limiting برای امنیت
- استفاده از JWT برای احراز هویت بدون وضعیت

### 🛡️ **امنیت**
- رمزگذاری قوی رمزهای عبور
- محدودیت زمانی برای OTP ها
- اعتبارسنجی کامل ورودی‌ها

### 📊 **مانیتورینگ**
- لاگ کامل عملیات احراز هویت
- ردیابی تلاش‌های ناموفق ورود
- آمار استفاده از API ها

---

## 🤝 **مشارکت در پروژه**

1. **Fork** کردن پروژه
2. ایجاد **Feature Branch** (`git checkout -b feature/new-feature`)
3. **Commit** تغییرات (`git commit -m 'Add new feature'`)
4. **Push** به Branch (`git push origin feature/new-feature`)
5. ایجاد **Pull Request**

---

<div align="center">

**⭐ اگر این پروژه مفید بود، حمایت خود را با ستاره نشان دهید!**

*ساخته شده با ❤️ برای جامعه توسعه‌دهندگان*

</div>