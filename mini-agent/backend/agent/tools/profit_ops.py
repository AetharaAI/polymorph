import asyncio
import csv
import json
import os
import re
import smtplib
import ssl
import uuid
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx

from backend.agent.tools.workspace import get_session_workspace

try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS


EMAIL_RE = re.compile(r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b")
PHONE_RE = re.compile(
    r"""
    (?:
        (?:\+?\d{1,3}[\s.\-]?)?
        (?:\(?\d{3}\)?[\s.\-]?)?
        \d{3}[\s.\-]?\d{4}
    )
    """,
    re.VERBOSE,
)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", flags=re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")

SAFE_MAIL_ALLOWLIST_DEFAULT = "aetherpro.us,aetherpro.tech"


def _normalize_url(url: str) -> str:
    value = (url or "").strip()
    if not value:
        return ""
    parsed = urlparse(value)
    if not parsed.scheme:
        value = f"https://{value}"
    return value


def _short_host(url: str) -> str:
    host = urlparse(url).netloc.lower().strip()
    if host.startswith("www."):
        host = host[4:]
    return host


def _strip_html(html: str) -> str:
    if not html:
        return ""
    text = TAG_RE.sub(" ", html)
    return WS_RE.sub(" ", text).strip()


def _dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        key = item.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(item.strip())
    return out


async def scrape_page(url: str, max_chars: int = 120000) -> str:
    """Fetch a web page and return raw html + cleaned text excerpt."""
    target = _normalize_url(url)
    if not target:
        return "Error: scrape_page requires a non-empty url."

    timeout_seconds = float(os.getenv("PROFIT_SCRAPE_TIMEOUT_SECONDS", "25"))
    max_chars = max(2000, min(int(max_chars), 500000))
    headers = {
        "User-Agent": os.getenv(
            "PROFIT_SCRAPER_USER_AGENT",
            "AetherPro-Agent/1.0 (+https://aetherpro.us)",
        )
    }

    allow_insecure_retry = _as_bool(os.getenv("PROFIT_SCRAPE_ALLOW_INSECURE_RETRY", "true"), default=True)
    insecure_used = False
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_seconds), follow_redirects=True) as client:
            resp = await client.get(target, headers=headers)
    except Exception as exc:
        msg = str(exc)
        if allow_insecure_retry and "CERTIFICATE_VERIFY_FAILED" in msg:
            try:
                async with httpx.AsyncClient(
                    timeout=httpx.Timeout(timeout_seconds),
                    follow_redirects=True,
                    verify=False,
                ) as client:
                    resp = await client.get(target, headers=headers)
                insecure_used = True
            except Exception as inner_exc:
                return f"Error: scrape_page failed after insecure retry: {inner_exc}"
        else:
            return f"Error: scrape_page failed: {exc}"

    raw_html = resp.text or ""
    html_limited = raw_html[:max_chars]
    clean_text = _strip_html(html_limited)[:max_chars]
    title_match = TITLE_RE.search(raw_html)
    title = WS_RE.sub(" ", title_match.group(1)).strip() if title_match else ""

    payload = {
        "url": target,
        "final_url": str(resp.url),
        "status_code": resp.status_code,
        "content_type": resp.headers.get("content-type", ""),
        "title": title,
        "html_char_count": len(raw_html),
        "html": html_limited,
        "text_excerpt": clean_text,
        "truncated": len(raw_html) > len(html_limited),
        "insecure_tls_retry_used": insecure_used,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(payload, indent=2)


def _extract_contacts_from_text(raw: str) -> dict[str, Any]:
    emails = _dedupe_keep_order(EMAIL_RE.findall(raw))
    phones = _dedupe_keep_order(PHONE_RE.findall(raw))
    filtered_emails = [
        e for e in emails
        if not e.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))
    ]
    return {
        "emails": filtered_emails[:200],
        "phones": phones[:200],
        "email_count": len(filtered_emails),
        "phone_count": len(phones),
    }


async def extract_contacts(html: str | None = None, url: str | None = None) -> str:
    """Extract emails and phone numbers from raw html/text or directly from a URL."""
    source_html = (html or "").strip()
    source_url = _normalize_url(url or "")

    if not source_html and not source_url:
        return "Error: extract_contacts requires either 'html' or 'url'."

    fetched: dict[str, Any] | None = None
    if not source_html and source_url:
        fetched_raw = await scrape_page(source_url)
        if fetched_raw.startswith("Error"):
            return fetched_raw
        try:
            fetched = json.loads(fetched_raw)
            source_html = str(fetched.get("html") or fetched.get("text_excerpt") or "")
        except Exception as exc:
            return f"Error: extract_contacts failed to parse scrape payload: {exc}"

    contacts = _extract_contacts_from_text(source_html)
    result = {
        "url": source_url or (fetched.get("final_url") if fetched else ""),
        "emails": contacts["emails"],
        "phones": contacts["phones"],
        "email_count": contacts["email_count"],
        "phone_count": contacts["phone_count"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(result, indent=2)


def _as_bool(raw: str, default: bool) -> bool:
    text = (raw or "").strip().lower()
    if not text:
        return default
    return text in {"1", "true", "yes", "on"}


def _send_email_sync(message: EmailMessage, smtp_host: str, smtp_port: int, use_ssl: bool, use_starttls: bool,
                     username: str, password: str) -> None:
    if use_ssl:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=30) as server:
            if username:
                server.login(username, password)
            server.send_message(message)
        return

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
        if use_starttls:
            context = ssl.create_default_context()
            server.starttls(context=context)
        if username:
            server.login(username, password)
        server.send_message(message)


async def send_email(
    to: str,
    subject: str,
    body: str,
    cc: str | None = None,
    bcc: str | None = None,
    reply_to: str | None = None,
    from_email: str | None = None,
    from_name: str | None = None,
    dry_run: bool = True,
) -> str:
    """Send (or preview) outreach email via SMTP."""
    recipient = (to or "").strip()
    if not recipient:
        return "Error: send_email requires 'to'."
    if not (subject or "").strip():
        return "Error: send_email requires 'subject'."
    if not (body or "").strip():
        return "Error: send_email requires 'body'."

    smtp_host = os.getenv("SMTP_HOST", "").strip()
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USERNAME", "").strip()
    smtp_pass = os.getenv("SMTP_PASSWORD", "").strip()
    smtp_use_ssl = _as_bool(os.getenv("SMTP_USE_SSL", "false"), default=False)
    smtp_use_starttls = _as_bool(os.getenv("SMTP_USE_STARTTLS", "true"), default=True)

    default_from_email = os.getenv("SMTP_FROM_EMAIL", "").strip()
    default_from_name = os.getenv("SMTP_FROM_NAME", "").strip()
    resolved_from_email = (from_email or default_from_email).strip()
    resolved_from_name = (from_name or default_from_name).strip()
    send_enabled = _as_bool(os.getenv("EMAIL_SEND_ENABLED", "false"), default=False)

    allowlist_raw = os.getenv("EMAIL_ALLOWED_DOMAIN_SUFFIXES", SAFE_MAIL_ALLOWLIST_DEFAULT)
    allowed_suffixes = [s.strip().lower() for s in allowlist_raw.split(",") if s.strip()]
    recipient_domain = recipient.split("@")[-1].lower() if "@" in recipient else ""
    allowlisted = any(recipient_domain.endswith(s) for s in allowed_suffixes) if recipient_domain else False

    preview = {
        "to": recipient,
        "subject": subject.strip(),
        "body_preview": body[:280],
        "cc": (cc or "").strip(),
        "bcc": bool((bcc or "").strip()),
        "reply_to": (reply_to or "").strip(),
        "from_email": resolved_from_email,
        "from_name": resolved_from_name,
        "dry_run": bool(dry_run),
        "send_enabled": send_enabled,
        "allowlisted_domain": allowlisted,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if dry_run:
        return json.dumps({"mode": "preview", "email": preview}, indent=2)

    if not send_enabled:
        return "Error: EMAIL_SEND_ENABLED is false. Use dry_run=true or enable sending explicitly."
    if not allowlisted:
        return (
            "Error: recipient domain is not allowlisted by EMAIL_ALLOWED_DOMAIN_SUFFIXES. "
            f"Recipient domain: {recipient_domain}"
        )
    if not smtp_host or not resolved_from_email:
        return "Error: SMTP_HOST and SMTP_FROM_EMAIL must be configured for send_email."
    if smtp_user and not smtp_pass:
        return "Error: SMTP_PASSWORD is required when SMTP_USERNAME is set."

    msg = EmailMessage()
    msg["To"] = recipient
    msg["From"] = f"{resolved_from_name} <{resolved_from_email}>" if resolved_from_name else resolved_from_email
    msg["Subject"] = subject.strip()
    if cc and cc.strip():
        msg["Cc"] = cc.strip()
    if reply_to and reply_to.strip():
        msg["Reply-To"] = reply_to.strip()
    msg["X-AetherPro-Lead-Outreach"] = "true"
    msg.set_content(body)

    try:
        await asyncio.to_thread(
            _send_email_sync,
            msg,
            smtp_host,
            smtp_port,
            smtp_use_ssl,
            smtp_use_starttls,
            smtp_user,
            smtp_pass,
        )
    except Exception as exc:
        return f"Error: send_email failed: {exc}"

    out = {
        "mode": "sent",
        "to": recipient,
        "subject": subject.strip(),
        "from_email": resolved_from_email,
        "smtp_host": smtp_host,
        "smtp_port": smtp_port,
        "message_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(out, indent=2)


def _lead_log_path(session_id: str, filename: str) -> Path:
    workspace = get_session_workspace(session_id)
    lead_dir = workspace / "profit"
    lead_dir.mkdir(parents=True, exist_ok=True)
    return lead_dir / filename


async def log_lead(
    session_id: str,
    company: str,
    email: str = "",
    niche: str = "",
    website: str = "",
    source_url: str = "",
    status: str = "new",
    notes: str = "",
    filename: str = "leads.csv",
) -> str:
    """Append a lead row to a workspace CSV log."""
    company = (company or "").strip()
    if not company:
        return "Error: log_lead requires 'company'."

    path = _lead_log_path(session_id, filename)
    row = {
        "lead_id": f"lead_{uuid.uuid4().hex[:12]}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "company": company,
        "email": (email or "").strip(),
        "niche": (niche or "").strip(),
        "website": (website or "").strip(),
        "source_url": (source_url or "").strip(),
        "status": (status or "new").strip(),
        "notes": (notes or "").strip(),
    }

    fieldnames = [
        "lead_id",
        "timestamp",
        "company",
        "email",
        "niche",
        "website",
        "source_url",
        "status",
        "notes",
    ]

    def _append() -> None:
        exists = path.exists()
        with path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not exists:
                writer.writeheader()
            writer.writerow(row)

    try:
        await asyncio.to_thread(_append)
    except Exception as exc:
        return f"Error: log_lead failed: {exc}"

    return json.dumps(
        {
            "ok": True,
            "path": str(path),
            "lead": row,
        },
        indent=2,
    )


async def list_leads(
    session_id: str,
    filename: str = "leads.csv",
    limit: int = 100,
    niche: str | None = None,
    status: str | None = None,
) -> str:
    """List recently logged leads from workspace CSV."""
    path = _lead_log_path(session_id, filename)
    if not path.exists():
        return json.dumps({"ok": True, "path": str(path), "count": 0, "leads": []}, indent=2)

    limit = max(1, min(int(limit), 1000))
    niche_filter = (niche or "").strip().lower()
    status_filter = (status or "").strip().lower()

    def _read() -> list[dict[str, str]]:
        with path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        return rows

    try:
        rows = await asyncio.to_thread(_read)
    except Exception as exc:
        return f"Error: list_leads failed: {exc}"

    filtered: list[dict[str, str]] = []
    for row in reversed(rows):
        if niche_filter and row.get("niche", "").strip().lower() != niche_filter:
            continue
        if status_filter and row.get("status", "").strip().lower() != status_filter:
            continue
        filtered.append(row)
        if len(filtered) >= limit:
            break

    return json.dumps(
        {
            "ok": True,
            "path": str(path),
            "count": len(filtered),
            "leads": filtered,
        },
        indent=2,
    )


async def run_campaign(
    session_id: str,
    niche: str,
    offer: str,
    geo: str = "",
    max_sites: int = 8,
    max_contacts_per_site: int = 2,
    dry_run: bool = True,
    send_limit: int = 10,
    filename: str = "leads.csv",
    subject_template: str | None = None,
    body_template: str | None = None,
) -> str:
    """One-click lead campaign runner: search -> scrape -> contacts -> log -> outreach."""
    niche = (niche or "").strip()
    offer = (offer or "").strip()
    if not niche:
        return "Error: run_campaign requires 'niche'."
    if not offer:
        return "Error: run_campaign requires 'offer'."

    max_sites = max(1, min(int(max_sites), 30))
    max_contacts_per_site = max(1, min(int(max_contacts_per_site), 10))
    send_limit = max(1, min(int(send_limit), 100))

    campaign_id = f"camp_{uuid.uuid4().hex[:12]}"
    query = f"{niche} {geo} contact email".strip()

    def _search() -> list[dict[str, str]]:
        with DDGS() as ddgs:
            raw = list(ddgs.text(query, max_results=max_sites * 2))
        out: list[dict[str, str]] = []
        seen_hosts: set[str] = set()
        for item in raw:
            url = item.get("href", item.get("url", "")).strip()
            title = item.get("title", "").strip()
            snippet = item.get("body", "").strip()
            if not url:
                continue
            host = _short_host(url)
            if not host or host in seen_hosts:
                continue
            seen_hosts.add(host)
            out.append({"url": url, "title": title, "snippet": snippet, "host": host})
            if len(out) >= max_sites:
                break
        return out

    try:
        sites = await asyncio.to_thread(_search)
    except Exception as exc:
        return f"Error: run_campaign search failed: {exc}"

    records: list[dict[str, Any]] = []
    emails_prepared = 0
    emails_sent = 0
    send_attempts = 0

    default_subject = f"{offer} for {niche}"
    for site in sites:
        scrape_raw = await scrape_page(site["url"], max_chars=140000)
        if scrape_raw.startswith("Error"):
            records.append(
                {
                    "site": site,
                    "status": "scrape_error",
                    "error": scrape_raw,
                    "emails": [],
                }
            )
            continue

        try:
            scraped = json.loads(scrape_raw)
        except Exception:
            records.append(
                {
                    "site": site,
                    "status": "scrape_parse_error",
                    "error": "Could not parse scrape payload",
                    "emails": [],
                }
            )
            continue

        contact_raw = await extract_contacts(html=scraped.get("html"), url=site["url"])
        if contact_raw.startswith("Error"):
            records.append(
                {
                    "site": site,
                    "status": "contact_error",
                    "error": contact_raw,
                    "emails": [],
                }
            )
            continue

        contact_data = json.loads(contact_raw)
        emails = list(contact_data.get("emails") or [])[:max_contacts_per_site]
        company = (scraped.get("title") or site.get("title") or site["host"]).strip()
        company = company[:120]

        site_record: dict[str, Any] = {
            "site": site,
            "company": company,
            "emails": [],
            "status": "no_contacts",
        }

        for email in emails:
            if send_attempts >= send_limit:
                break
            send_attempts += 1
            emails_prepared += 1

            subject = (subject_template or default_subject).format(
                niche=niche,
                offer=offer,
                company=company,
                geo=geo,
                host=site["host"],
            )
            body = (
                body_template
                or (
                    "Hi {company},\n\n"
                    "We help {niche} teams with {offer}.\n"
                    "If useful, I can share a quick 5-minute breakdown specific to your workflow.\n\n"
                    "Best,\nAetherPro"
                )
            ).format(
                niche=niche,
                offer=offer,
                company=company,
                geo=geo,
                host=site["host"],
            )

            mail_raw = await send_email(
                to=email,
                subject=subject,
                body=body,
                dry_run=dry_run,
            )
            mail_ok = not str(mail_raw).startswith("Error")
            if mail_ok and not dry_run:
                emails_sent += 1

            lead_status = "outreach_preview" if dry_run else ("emailed" if mail_ok else "email_error")
            await log_lead(
                session_id=session_id,
                company=company,
                email=email,
                niche=niche,
                website=site["url"],
                source_url=site["url"],
                status=lead_status,
                notes=f"campaign_id={campaign_id}",
                filename=filename,
            )

            site_record["emails"].append(
                {
                    "to": email,
                    "mail_result": json.loads(mail_raw) if mail_ok and mail_raw.strip().startswith("{") else mail_raw,
                }
            )

        if site_record["emails"]:
            site_record["status"] = "processed"
        site_record["contact_email_count"] = len(emails)
        records.append(site_record)

        if send_attempts >= send_limit:
            break

    summary = {
        "campaign_id": campaign_id,
        "query": query,
        "niche": niche,
        "offer": offer,
        "geo": geo,
        "dry_run": bool(dry_run),
        "sites_scanned": len(sites),
        "send_limit": send_limit,
        "emails_prepared": emails_prepared,
        "emails_sent": emails_sent,
        "lead_log_path": str(_lead_log_path(session_id, filename)),
        "records": records,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(summary, indent=2)
