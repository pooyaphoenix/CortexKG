<p align="center">

  <img width="800" height="500" alt="CortexKG" src="https://github.com/user-attachments/assets/2a57efda-9239-4052-8e35-a2cbdff16a5d" />

</p>

<div dir="rtl" align="center">

<b>CortexKG: حافظه قابل‌حمل هوش مصنوعی با قدرت Knowledge Graph</b>

<br><br>

<a href="https://github.com/pooyaphoenix/CortexKG/releases">
  <img src="https://img.shields.io/github/v/release/pooyaphoenix/CortexKG?color=blue&label=version" alt="Release Version"/>
</a>

<a href="https://github.com/pooyaphoenix/CortexKG/stargazers">
  <img src="https://img.shields.io/github/stars/pooyaphoenix/CortexKG?style=social" alt="GitHub stars"/>
</a>

<a href="mailto:pooyachavoshi@gmail.com">
  <img src="https://img.shields.io/badge/Email-Contact-blue?style=flat&logo=gmail" alt="Email"/>
</a>

</div>

---

<div dir="rtl" align="right">

# 🧠 CortexKG

## ساخت یک Knowledge Graph زنده برای مکالمات شما با هوش مصنوعی

مکالمات خود را به یک **Knowledge Graph پایدار** تبدیل کنید و به <bdi>LLM</bdi>ها حافظه بلندمدت بر پایه **دانش، روابط و context شخصی خودتان** بدهید.

---

# چرا CortexKG؟

</div>

https://github.com/user-attachments/assets/3b3ed74f-f3cf-4d5d-88cf-af9caef9eeb8

<div dir="rtl" align="right">

مدل‌های زبانی بزرگ یا <bdi>Large Language Models</bdi> بسیار قدرتمند هستند، اما یک محدودیت مهم دارند:

آن‌ها واقعاً **شما را نمی‌شناسند**.

اگر context را به‌صورت دستی در اختیار مدل قرار ندهید یا به پنجره‌های context طولانی و پرهزینه متکی نباشید، تقریباً هر مکالمه از ابتدا شروع می‌شود.

<bdi>CortexKG</bdi> رویکرد متفاوتی را ارائه می‌دهد.

به‌جای اینکه بارها به مدل بگویید چه کسی هستید، چه چیزهایی می‌دانید، چه چیزهایی یاد گرفته‌اید و مفاهیم مختلف چگونه به یکدیگر مرتبط هستند، <bdi>CortexKG</bdi> به‌صورت مداوم دانش موجود در مکالمات شما را استخراج کرده و آن را به شکل یک **گراف از entityها و relationshipها** ذخیره می‌کند.

با گذشت زمان، دستیار هوش مصنوعی شما چیزی شبیه‌تر به یک **نمایش دیجیتال از ذهن شما** ایجاد می‌کند؛ نه اینکه صرفاً تاریخچه چت‌های قبلی را نگه دارد.

---

# CortexKG چه کاری انجام می‌دهد؟

</div>

<img width="800" height="400" alt="Screenshot 2026-08-07 213124" src="https://github.com/user-attachments/assets/5e0f2078-f824-4218-b5a7-7226f0d477b5" />

<div dir="rtl" align="right">

در هر مکالمه:

</div>

<div dir="rtl" align="right">

1. با <bdi>LLM</bdi> مورد علاقه خود گفتگو می‌کنید.
2. <bdi>CortexKG</bdi>، entityها و relationshipها را استخراج می‌کند.
3. این relationshipها در یک Knowledge Graph ذخیره می‌شوند — **همراه با timestampی که دقیقاً مشخص می‌کند هر بخش از دانش چه زمانی یاد گرفته شده است.**
4. می‌توانید memoryهای ذخیره‌شده را مشاهده، بررسی و مدیریت کنید.
5. در مکالمات بعدی، این graph می‌تواند دوباره به‌عنوان context در اختیار <bdi>LLM</bdi> قرار گیرد.
6. گراف هم‌زمان با یادگیری و ارتباط شما، به‌صورت مداوم تکامل پیدا می‌کند.

<bdi>CortexKG</bdi> به‌جای ذخیره صرفاً متن، **دانش** را ذخیره می‌کند — و علاوه بر اینکه می‌داند *چه چیزی* را یاد گرفته، به یاد دارد *چه زمانی* آن را یاد گرفته است.

---

# ✨ قابلیت‌ها

## Memory & Knowledge

* 🧠 **Persistent AI Memory** — ذخیره دانش حاصل از مکالمات به‌عنوان یک Knowledge Graph زنده.
* ⏱️ **Temporal Memory** — هر entity و relationship دارای timestamp مربوط به اولین زمان یادگیری و آخرین زمان اشاره به آن است.
* 🗂️ **Memory Control Center** — جستجو، فیلتر، مرتب‌سازی، ویرایش، تأیید، رد و حذف memoryها.
* ✅ **Memory Review** — علامت‌گذاری memoryهای استخراج‌شده به‌عنوان confirmed، unreviewed یا rejected.
* 🔄 **Portable Memory** — export و import کردن Knowledge Graph به‌صورت JSON.
* 🧩 **Graph-Based Context** — استفاده از دانش ذخیره‌شده به‌عنوان context برای مکالمات آینده با <bdi>LLM</bdi>.

## Visualization

* 🌐 **3D Knowledge Graph Explorer** — حرکت، zoom و گردش در Knowledge Graph به‌صورت سه‌بعدی.
* 🏷️ **Always-Visible Labels** — نام entityها و relationshipها مستقیماً در محیط نمایش داده می‌شوند و نیازی به hover نیست.
* ⏳ **Timeline Scrubber & Playback** — بازگرداندن graph به هر نقطه از زمان و مشاهده شکل‌گیری تدریجی آن.
* 🎨 **Dual Color Modes** — رنگ‌آمیزی nodeها بر اساس وضعیت review یا سن آن‌ها.
* 📊 **Knowledge Timeline Panel** — نمایش تعداد entityهای جدید یادگرفته‌شده در هر روز به همراه یک log کامل chronological.
* 🔀 **2D / 3D Toggle** — امکان جابه‌جایی بین نمای 2D و 3D.

## Models & Control

* 💬 **Multi-Provider LLM Support** — پشتیبانی از Ollama، OpenAI، Gemini و APIهای سازگار با OpenAI.
* 🌡️ **Per-Provider Generation Settings** — تنظیم مستقل temperature و حداکثر تعداد token برای هر provider.
* 📝 **Custom System Prompt** — تعریف system instruction اختصاصی یا استفاده از سطوح detail داخلی.
* 🔒 **Local-First Support** — استفاده از Ollama برای inference محلی و ذخیره‌سازی local memory.

---

# 🌐 3D Knowledge Graph Explorer

Knowledge Graph شما با استفاده از **Three.js / WebGL** به شکل یک interactive 3D force-directed graph نمایش داده می‌شود.

این محیط به clusterهای متراکم اجازه می‌دهد از یکدیگر فاصله بگیرند؛ چیزی که در layoutهای ساده 2D محدودتر است.

### کنترل‌های Explorer

| عملیات              | کنترل                                         |
| :------------------ | :-------------------------------------------- |
| چرخاندن             | Drag                                          |
| Zoom                | Scroll                                        |
| حرکت دادن صفحه      | Right-drag                                    |
| تمرکز روی یک entity | Click روی node — دوربین به سمت آن حرکت می‌کند |
| بازنشانی دوربین     | 🎯 Reset View                                 |
| بزرگ‌نمایی محیط     | ⛶ Fullscreen                                  |

### نمایش بصری اطلاعات

* **رنگ Node** — وضعیت review را نشان می‌دهد: ✅ confirmed / 🟡 unreviewed / ❌ rejected. همچنین می‌توان رنگ‌بندی را بر اساس age تغییر داد.
* **اندازه Node** — تعداد connectionها را نشان می‌دهد تا entityهای مرکزی و مهم سریع‌تر قابل تشخیص باشند.
* **فلش‌های جهت‌دار و particleهای متحرک** — جهت relationshipها را به‌صورت واضح نمایش می‌دهند.
* **Floating Labels** — نام entityها و نوع relationshipها همیشه قابل مشاهده هستند.

اگر graph شما بسیار متراکم است و نمای ساده‌تر را ترجیح می‌دهید، renderer دوبعدی تنها با یک toggle در دسترس است.

---

# ⏳ Temporal Memory

دانستن اینکه هوش مصنوعی شما *چه چیزی* را به خاطر دارد مفید است.

اما دانستن اینکه *چه زمانی* آن را یاد گرفته، چیزی است که memory را **قابل بررسی و audit** می‌کند.

هر node و edge در graph دارای اطلاعات زیر است:

* **`created_at`** — زمانی که این دانش برای اولین بار وارد graph شده است.
* **`updated_at`** — آخرین مکالمه‌ای که در آن به این دانش اشاره شده است.
* **`mention_count`** — تعداد دفعاتی که این دانش در مکالمات ظاهر شده است.

## Time-Travel Scrubber

نمای 3D دارای یک timeline control در پایین canvas است.

می‌توانید slider را حرکت دهید تا graph را به هر نقطه‌ای از تاریخچه آن برگردانید، یا دکمه **▶** را فشار دهید تا شکل‌گیری Knowledge Graph را به‌صورت chronological از اولین entity تا جدیدترین entity مشاهده کنید.

به‌جای اینکه layout در هر frame دوباره ساخته شود، scrubber تنها visibility مربوط به nodeها را تغییر می‌دهد.

در نتیجه، ساختار فضایی graph پایدار باقی می‌ماند و entityها به مرور زمان ظاهر می‌شوند.

## Knowledge Timeline Panel

در زیر graph، یک timeline panel قابل باز شدن قرار دارد که شامل موارد زیر است:

* نمودار تعداد entityهای جدیدی که در هر روز یاد گرفته شده‌اند.
* یک log کامل chronological شامل first-seen، last-mentioned و mention count برای هر entity.

> **نکته درباره graphهای موجود:** دانش‌هایی که قبل از اضافه شدن این قابلیت ثبت شده‌اند، به‌صورت صادقانه با مقدار `unknown` نمایش داده می‌شوند و تاریخ جعلی برای آن‌ها ایجاد نمی‌شود. این موارد همچنان به‌صورت دائمی در timeline scrubber قابل مشاهده هستند.

---

# 🧠 مدیریت Memory

<bdi>CortexKG</bdi> به شما کنترل مستقیم روی چیزهایی که هوش مصنوعی به خاطر می‌سپارد می‌دهد.

</div>

<img width="800" height="390" alt="VideoProject7-ezgif com-crop" src="https://github.com/user-attachments/assets/c8b46c63-f05f-480e-b08f-97c9ec5c586b" />

<div dir="rtl" align="right">

از طریق **Memory Control Center** می‌توانید:

* 🔎 memoryها را جستجو و filter کنید.
* 🔃 بر اساس recently updated، recently created، most mentioned یا name مرتب‌سازی کنید.
* ✏️ label و entity type مربوط به memoryها را ویرایش کنید.
* ✅ memoryها را تأیید کنید.
* ❌ memoryها را رد کنید.
* 🗑️ memoryها را حذف کنید.
* 🔗 relationshipها را بررسی کنید، از جمله زمانی که هر relationship برای اولین بار مشاهده شده است.
* 📅 زمان اولین یادگیری و آخرین اشاره به هر memory را مشاهده کنید.
* 📊 آمار مربوط به memoryها را مشاهده کنید.

این قابلیت‌ها باعث می‌شوند memory در <bdi>CortexKG</bdi> **شفاف، قابل ویرایش و کاملاً تحت کنترل کاربر** باشد.

---

# ⚙️ تنظیمات

تمام تنظیمات در sidebar قرار دارند و به‌صورت خودکار در `app_config.json` ذخیره می‌شوند — بدون نیاز به restart کردن برنامه.

## 🤖 Model & Connection

این بخش همیشه در دسترس است و می‌توانید provider، نام model و اطلاعات connection را مشخص کنید.

| تنظیم        | توضیح                                                                                              |
| :----------- | :------------------------------------------------------------------------------------------------- |
| LLM Provider | Ollama، OpenAI، Google Gemini یا یک endpoint سفارشی سازگار با OpenAI                               |
| Model Name   | شناسه model برای هر provider                                                                       |
| Base URL     | برای Ollama و endpointهای سفارشی                                                                   |
| API Key      | برای هر provider به‌صورت جداگانه ذخیره می‌شود تا هنگام تغییر provider نیازی به ورود مجدد key نباشد |

## 🎛️ Generation & Prompt

| تنظیم                 | توضیح                                                                                                                          |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| Temperature           | مقدار `0.0` تا `2.0` که برای هر provider به‌صورت جداگانه ذخیره می‌شود. Presetهای آماده: 🎯 Precise · ⚖️ Balanced · 🎨 Creative |
| Max Tokens            | محدودیت طول response که به parameter مربوط به backend تبدیل می‌شود                                                             |
| Response Detail Level | دستورهای داخلی برای پاسخ‌های Short / Medium / Long                                                                             |
| Custom System Prompt  | instruction اختصاصی شما که در صورت پر بودن، Response Detail Level را override می‌کند                                           |

مقدار Max Tokens متناسب با backend مورد استفاده ترجمه می‌شود:

* `max_tokens` برای APIهای سازگار با OpenAI
* `max_output_tokens` برای Gemini
* `num_predict` برای Ollama

## 🧠 رفتار Knowledge Graph

| تنظیم                          | توضیح                                                                       |
| :----------------------------- | :-------------------------------------------------------------------------- |
| Use Graph as Knowledge Context | entityها و relationshipهای ذخیره‌شده را وارد system prompt می‌کند           |
| Build Graph From               | استخراج اطلاعات فقط از user input یا از user input به همراه model responses |

## 💾 Data & Memory

می‌توانید graph خود را به‌صورت JSON export کنید، یک export قبلی را import کنید یا تمام تنظیمات را به حالت پیش‌فرض بازگردانید.

---

# Supported Providers

در حال حاضر <bdi>CortexKG</bdi> از providerهای زیر پشتیبانی می‌کند:

* Ollama (Local)
* OpenAI
* Google Gemini
* هر API سازگار با OpenAI

نمونه‌ها:

* OpenRouter
* LM Studio
* vLLM
* ArvanCloud
* Local OpenAI-compatible servers

---

# 🚀 نصب

## 1. 🐳 اجرای پروژه با Docker — روش پیشنهادی

</div>

```bash
git clone https://github.com/pooyaphoenix/CortexKG.git

cd CortexKG

docker compose up -d
```

<div dir="rtl" align="right">

سپس **<bdi>http://localhost:8501</bdi>** را باز کنید.

تنظیمات، API keyها و Knowledge Graph شما در یک Docker volume ذخیره می‌شوند و پس از restart نیز باقی می‌مانند.

> **استفاده از Ollama؟**
>
> از داخل container، عبارت `localhost` به خود container اشاره می‌کند.
>
> در بخش Settings مقدار Ollama Base URL را روی
> `http://host.docker.internal:11434`
> قرار دهید تا به یک instance از Ollama که روی سیستم اصلی شما اجرا می‌شود دسترسی پیدا کند.
>
> یا می‌توانید سرویس اختیاری `ollama` را در `docker-compose.yml` از حالت comment خارج کنید تا Ollama نیز کاملاً داخل container اجرا شود.

---

## 2. Clone کردن repository

</div>

```bash
git clone https://github.com/pooyaphoenix/CortexKG.git

cd CortexKG
```

<div dir="rtl" align="right">

---

## 3. ساخت virtual environment

### Windows

</div>

```bash
python -m venv .venv
.venv\Scripts\activate
```

<div dir="rtl" align="right">

### Linux / macOS

</div>

```bash
python3 -m venv .venv
source .venv/bin/activate
```

<div dir="rtl" align="right">

---

## 4. نصب dependencies

</div>

```bash
pip install -r requirements.txt
```

<div dir="rtl" align="right">

---

## 5. اجرای application

</div>

```bash
python main.py
```

<div dir="rtl" align="right">

برنامه به‌صورت خودکار <bdi>Streamlit</bdi> را اجرا خواهد کرد.

> renderer مربوط به graph سه‌بعدی به‌صورت client-side از طریق CDN بارگذاری می‌شود؛ بنابراین **هیچ Python dependency جدیدی** به محیط شما اضافه نمی‌کند.

---

# 🤝 مشارکت در پروژه

از contributionها همیشه استقبال می‌شود.

چه در زمینه:

* bug fix
* بهبود UI
* اضافه کردن providerهای جدید
* documentation
* الگوریتم‌های graph
* بهینه‌سازی memory
* entity resolution و deduplication

می‌توانید یک issue ایجاد کنید یا یک pull request ارسال کنید.

---

# Philosophy

<bdi>CortexKG</bdi> بر پایه یک ایده ساده ساخته شده است:

> **دانش شما باید متعلق به خودتان باشد.**

سیستم‌های AI باید چیزهایی را که **خودتان انتخاب می‌کنید** به خاطر بسپارند، ارتباط میان ایده‌های شما را درک کنند و به شما اجازه دهند این memory را بین modelها و providerهای مختلف جابه‌جا کنید.

Memory شما نباید زمانی که از GPT به Gemini، از Claude به Ollama، یا از یک platform به platform دیگر منتقل می‌شوید، ناپدید شود.

هدف <bdi>CortexKG</bdi> این است که memory شخصی AI را:

* **قابل‌حمل (Portable)**
* **شفاف (Transparent)**
* **تحت مالکیت کاربر (User-Owned)**

کند.

---

# License

این پروژه تحت **MIT License** منتشر شده است.

---

## Email

[pooyachavoshi@gmail.com](mailto:pooyachavoshi@gmail.com)

اگر این پروژه برای شما مفید است، با دادن یک ⭐ از توسعه آینده آن حمایت کنید.

</div>
