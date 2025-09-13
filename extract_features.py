import re
import urllib.parse
from confusable_homoglyphs import confusables

# Trusted domains for homoglyph comparison
TRUSTED_DOMAINS = [
    "google.com", "facebook.com", "paypal.com", "amazon.com", "github.com",
    "linkedin.com", "apple.com", "microsoft.com", "netflix.com", "youtube.com",
    "instagram.com", "wikipedia.org", "twitter.com", "adobe.com", "dropbox.com",
    "quora.com", "slack.com", "trello.com", "medium.com", "salesforce.com",
    "tesla.com", "adidas.com", "nike.com", "khanacademy.org", "udemy.com",
    "coursera.org", "edx.org", "walmart.com", "ebay.com", "samsung.com",
    "intel.com", "oracle.com", "sony.com", "tiktok.com", "mozilla.org",
    "zillow.com", "chase.com", "bankofamerica.com", "capitalone.com", "hsbc.com",
    "uber.com", "lyft.com", "cnn.com", "bbc.com", "nytimes.com", "espn.com",
    "booking.com", "airbnb.com", "stackoverflow.com", "github.io", "icann.org",
    "getbootstrap.com", "npmjs.com"
]

# List of features expected by the ML model
REQUIRED_FEATURES = [
    "url_length", "has_ip", "has_at", "has_https_token", "has_prefix_suffix",
    "subdomain_count", "slash_count", "dot_count", "is_long_url", "is_short_url", "has_homoglyph"
]

def extract_features(url):
    features = {}
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.lower().replace("www.", "")

    features["url_length"] = len(url)
    features["has_ip"] = int(bool(re.search(r"(\d{1,3}\.){3}\d{1,3}", domain)))
    features["has_at"] = int("@" in url)
    features["has_https_token"] = int("https" in domain)
    features["has_prefix_suffix"] = int("-" in domain)
    features["subdomain_count"] = domain.count(".") - 1
    features["slash_count"] = url.count("/")
    features["dot_count"] = url.count(".")
    features["is_long_url"] = int(len(url) > 75)
    features["is_short_url"] = int(len(url) < 25)

    # ✅ Final homoglyph detection (safely ignores exact matches)
    features["has_homoglyph"] = 0
    for trusted in TRUSTED_DOMAINS:
        if domain != trusted and confusables.is_confusable(domain, trusted):
            features["has_homoglyph"] = 1
            break

    # Ensure all required features exist
    for key in REQUIRED_FEATURES:
        features.setdefault(key, 0)

    return features
