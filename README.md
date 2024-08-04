# بررسی در دسترس بودن دامنه‌ها

این اسکریپت یک لیست از نام دامنه‌ها را از یک فایل JSON می‌خواند، هر دامنه را پینگ می‌کند تا ببیند آیا فعال است یا خیر، و دامنه‌های فعال را به یک فایل متنی می‌نویسد. هدف این اسکریپت خودکارسازی فرآیند شناسایی دامنه‌های فعال از یک مجموعه داده‌ است.

## پیش‌نیازها

برای اجرای این اسکریپت، نیاز به نصب پایتون بر روی سیستم خود دارید. همچنین، اسکریپت از ماژول `subprocess` که در کتابخانه استاندارد پایتون قرار دارد، استفاده می‌کند.

## فایل‌ها

- `domains.json`: فایل ورودی که شامل لیست دامنه‌های مورد بررسی است. این فایل باید به فرمت زیر باشد:
    ```json
    {
        "data": [
            {"domain": "example.com"},
            {"domain": "example.org"},
            ...
        ]
    }
    ```
- `active_domains.txt`: فایل خروجی که دامنه‌های فعال در آن نوشته خواهند شد.

## توضیحات اسکریپت

این اسکریپت مراحل زیر را انجام می‌دهد:

1. **خواندن فایل JSON**: اسکریپت فایل `domains.json` را باز کرده و نام دامنه‌ها را استخراج می‌کند.
    ```python
    with open('domains.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        domains = [entry['domain'] for entry in data['data']]
    ```

2. **پینگ کردن هر دامنه**: برای هر دامنه در لیست، اسکریپت یک دستور پینگ با استفاده از ماژول `subprocess` اجرا می‌کند. خروجی را می‌گیرد و بررسی می‌کند که آیا پینگ موفق بوده است یا خیر.
    ```python
    def ping_domain(domain):
        try:
            result = subprocess.run(['ping', '-n', '4', domain], capture_output=True, text=True)
            output = result.stdout
            if "Destination net unreachable" in output or "Request timed out" in output:
                return False
            if "Received = 4" in output:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error pinging {domain}: {e}")
            return False
    ```

3. **نوشتن دامنه‌های فعال به فایل**: اسکریپت دامنه‌های فعال را به `active_domains.txt` می‌نویسد. دامنه‌ها را بررسی کرده، و در صورت فعال بودن به فایل خروجی اضافه می‌کند.
    ```python
    with open(output_file, 'w', encoding='utf-8') as file:
        for domain in domains:
            if ping_domain(domain):
                file.write(f"{domain}\n")
                print(f"{domain} is active and saved.")
            else:
                print(f"{domain} is not active.")
    ```

4. **پیام اتمام**: در نهایت، اسکریپت پیامی مبنی بر اتمام پردازش چاپ می‌کند.
    ```python
    print("Processing complete.")
    ```

## اجرای اسکریپت

برای اجرای اسکریپت، کافی است آن را با پایتون اجرا کنید:
```sh
python domain_checker.py
