import PyPDF2
from textblob import TextBlob
import re

# Load and extract PDF text
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Sentiment Analysis
def sentiment_analysis(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"

# Extract Financial Metrics and Profitability Indicators
def extract_financial_info(text):
    # Example regular expressions to find profitability terms
    profit_keywords = ["net income", "earnings", "profit", "loss"]
    for keyword in profit_keywords:
        occurrences = re.findall(rf"\b{keyword}\b.*?\b\d+[.,]?\d*\b", text, re.IGNORECASE)
        print(f"Occurrences for {keyword.capitalize()}: {occurrences}")

# Extract Investment Companies
def extract_invested_companies(text):
    # Use simple regex to find "invested in X company"
    investments = re.findall(r"\binvested in\b.*?\b[A-Z][a-z]*\b", text)
    return investments

# Run analysis
pdf_text = extract_text_from_pdf("recent_report.pdf")
print("Sentiment:", sentiment_analysis(pdf_text))
extract_financial_info(pdf_text)
print("Invested Companies:", extract_invested_companies(pdf_text))