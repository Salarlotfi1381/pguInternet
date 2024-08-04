import json
import subprocess

# خواندن فایل JSON
with open('domains.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    domains = [entry['domain'] for entry in data['data']]

# تابع برای اجرای دستور ping
def ping_domain(domain):
    try:
        # اجرای دستور ping
        result = subprocess.run(['ping', '-n', '4', domain], capture_output=True, text=True)
        
        # بررسی نتیجه
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

# فایل خروجی برای ذخیره دامنه‌هایی که پاسخ می‌دهند
output_file = 'active_domains.txt'

# پردازش دامنه‌ها
with open(output_file, 'w', encoding='utf-8') as file:
    for domain in domains:
        if ping_domain(domain):
            file.write(f"{domain}\n")
            print(f"{domain} is active and saved.")
        else:
            print(f"{domain} is not active.")

print("Processing complete.")
