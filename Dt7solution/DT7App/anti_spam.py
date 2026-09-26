import time
import re
from django.core.cache import cache
from .models import SpamSubmissionLog

# Honeypot field names to trap automated spam bots
HONEYPOT_FIELDS = [
    "website_hp",
    "hp_website_url",
    "hp_email_confirm",
    "user_phone_hp",
    "fax_number_hp"
]

# Blacklisted spam keywords / phrases common in AI & bot submissions
SPAM_KEYWORDS = [
    "http://", "https://", "[url=", "<a href=", "href=",
    "casino", "crypto", "bitcoin", "backlink", "seo ranking",
    "ranking #1", "viagra", "whatsapp group", "telegram channel",
    "earn money", "passive income", "guest post", "marketing list",
    "domain sale", "loan approval", "dating app", "pills",
    "lorem ipsum", "test test test", "asdfgh", "qwertyuiop"
]

# Blacklisted email TLDs / disposable email provider domains
SPAM_EMAIL_DOMAINS = [
    "mailinator.com", "guerrillamail.com", "tempmail.org", "tempmail.com",
    "10minutemail.com", "dispostable.com", "sharklasers.com", "yopmail.com",
    "trashmail.com", "getairmail.com", "throwawaymail.com"
]

SPAM_TLDS = [".ru", ".xyz", ".top", ".tk", ".work", ".click", ".monster", ".gq", ".cf", ".ml"]

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')

def is_spam_submission(request, form_name="Form", name="", email="", message="", extra_data=None):
    """
    Evaluates submission for automated bot or AI dummy spam.
    Returns (is_spam: bool, reason: str)
    """
    post_data = request.POST
    ip = get_client_ip(request)

    # 0. Math Calculation Security Verification check
    math_num1 = post_data.get("math_num1")
    math_num2 = post_data.get("math_num2")
    math_answer = post_data.get("math_answer")

    if math_num1 is not None and math_num2 is not None:
        try:
            expected_sum = int(math_num1) + int(math_num2)
            user_ans = int(math_answer.strip()) if (math_answer and math_answer.strip().isdigit()) else None
            if user_ans != expected_sum:
                log_spam(form_name, name, email, ip, f"Incorrect Math Calculation: {user_ans} != {expected_sum} ({math_num1} + {math_num2})", post_data)
                return True, "Incorrect math calculation answer"
        except (ValueError, TypeError):
            log_spam(form_name, name, email, ip, "Invalid Math Calculation input values", post_data)
            return True, "Invalid math calculation answer"

    # 0b. Visual Security Code CAPTCHA check
    captcha_expected = post_data.get("captcha_expected", "").strip().upper()
    captcha_input = post_data.get("captcha_input", "").strip().upper()

    if captcha_expected:
        if not captcha_input or captcha_input != captcha_expected:
            log_spam(form_name, name, email, ip, f"Incorrect CAPTCHA Code: '{captcha_input}' != '{captcha_expected}'", post_data)
            return True, "Incorrect visual CAPTCHA security code"

    # 1. Honeypot check

    for hp_field in HONEYPOT_FIELDS:
        if post_data.get(hp_field, "").strip():
            log_spam(form_name, name, email, ip, f"Honeypot field '{hp_field}' filled", post_data)
            return True, f"Honeypot trap triggered ({hp_field})"


    # 2. Time-trap check (submitted too fast < 2.5s)
    render_ts_str = post_data.get("form_render_ts", "")
    if render_ts_str:
        try:
            render_ts = float(render_ts_str)
            time_taken = time.time() - render_ts
            if time_taken < 2.5:
                log_spam(form_name, name, email, ip, f"Form submitted in {time_taken:.2f}s (< 2.5s time trap)", post_data)
                return True, "Form submitted too fast (automated bot)"
        except (ValueError, TypeError):
            pass

    # 3. Rate limiting check (max 5 form submissions per IP in 10 minutes)
    cache_key = f"anti_spam_rate_{ip}"
    submission_count = cache.get(cache_key, 0)
    if submission_count >= 5:
        log_spam(form_name, name, email, ip, "IP Rate Limit Exceeded (> 5 submissions in 10 min)", post_data)
        return True, "Too many submissions from this IP address"

    # 4. Email format & domain analysis
    email_lower = (email or "").strip().lower()
    if email_lower:
        for domain in SPAM_EMAIL_DOMAINS:
            if email_lower.endswith("@" + domain) or domain in email_lower:
                log_spam(form_name, name, email, ip, f"Disposable email domain: {domain}", post_data)
                return True, "Disposable or suspicious email address"

        for tld in SPAM_TLDS:
            if email_lower.endswith(tld):
                log_spam(form_name, name, email, ip, f"Suspicious email TLD: {tld}", post_data)
                return True, "Suspicious email TLD domain"

    # 5. Content & Spam Keyword Analysis
    combined_text = f"{name} {email} {message}".lower()
    for kw in SPAM_KEYWORDS:
        if kw in combined_text:
            log_spam(form_name, name, email, ip, f"Spam keyword found: '{kw}'", post_data)
            return True, f"Contains spam keyword: '{kw}'"

    # 6. Check for excessive URLs in message (> 1 link)
    urls_in_msg = re.findall(r'https?://|www\.', message or "", re.IGNORECASE)
    if len(urls_in_msg) > 1:
        log_spam(form_name, name, email, ip, f"Excessive links in message ({len(urls_in_msg)} links)", post_data)
        return True, "Too many links in message"

    # 7. Check for gibberish / bot name pattern (e.g. 8+ chars without spaces or vowels like Xg9zLq3wP82)
    clean_name = (name or "").strip()
    if len(clean_name) > 8 and not " " in clean_name and not re.search(r'[aeiouyAEIOUY]', clean_name):
        log_spam(form_name, name, email, ip, f"Gibberish name pattern: '{clean_name}'", post_data)
        return True, "Suspicious gibberish name pattern"

    # Update rate limit counter
    cache.set(cache_key, submission_count + 1, 600)  # 10 minutes TTL
    return False, "Clean"


def log_spam(form_name, name, email, ip, reason, raw_post_data):
    try:
        data_dict = {}
        if raw_post_data:
            for k, v in raw_post_data.items():
                if k not in ["csrfmiddlewaretoken"]:
                    data_dict[k] = str(v)[:200]
        SpamSubmissionLog.objects.create(
            form_name=form_name,
            name=(name or "")[:250],
            email=(email or "")[:250],
            ip_address=ip,
            reason=reason[:250],
            submitted_data=data_dict
        )
    except Exception as e:
        print(f"AntiSpam Log Error: {e}")
