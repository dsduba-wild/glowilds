"""Check the contact form script (assets/js/scripts.js) without sending anything to Formspree.

Usage: hugo server, then  python3 design/contact_form_check.py [contact page URL]   (needs: pip install playwright)
A fake Formspree first accepts (the page must thank the visitor and clear the form), then refuses
(the form must fall back to a normal post, so the request still goes through).
"""
import shutil
import sys
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:1313/contact/"
FIELDS = {"#cf-name": "Test", "#cf-email": "t@example.com", "#cf-business": "Biz", "#cf-phone": "720", "#cf-message": "hi"}

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=shutil.which("chromium"))  # system Chromium if present, else Playwright's
    for status in (200, 403):
        page = browser.new_page()
        seen = []

        def fake_formspree(route, req, status=status):
            seen.append(req.resource_type)
            if req.resource_type == "fetch":
                route.fulfill(status=status, content_type="application/json", body="{}")
            else:
                route.fulfill(status=200, content_type="text/html", body="formspree page")

        page.route("https://formspree.io/**", fake_formspree)
        page.goto(URL)
        for field, value in FIELDS.items():
            page.fill(field, value)
        page.click(".contact-submit")
        page.wait_for_timeout(1500)
        if status == 200:
            assert seen == ["fetch"], seen
            assert "sent" in page.inner_text(".contact-status"), "no thank-you line"
            assert page.input_value("#cf-name") == "", "form not cleared"
        else:
            assert seen == ["fetch", "document"], seen
            assert page.url.startswith("https://formspree.io/"), page.url
        print(f"Formspree {status}: ok")
    browser.close()
