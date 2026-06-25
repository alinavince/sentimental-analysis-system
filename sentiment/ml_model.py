"""
ml_model.py  –  Train, save, and predict with the Sentiment Analysis ML pipeline.

Model: Logistic Regression (best overall for text classification)
       with TF-IDF vectorizer (unigrams + bigrams)

Usage:
    python train_model.py          ← run once to generate model files
    from sentiment.ml_model import predict_sentiment   ← use in views
"""

import os
import re
import string
import joblib
import numpy as np
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
MODEL_DIR   = Path(__file__).resolve().parent / 'ml_models'
MODEL_PATH  = MODEL_DIR / 'sentiment_model.pkl'
VECTORIZER_PATH = MODEL_DIR / 'tfidf_vectorizer.pkl'


# ─── Text Preprocessing ───────────────────────────────────────────────────────
def clean_text(text: str) -> str:
    """Lowercase, remove URLs, punctuation, extra spaces."""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)         # remove URLs
    text = re.sub(r'<.*?>', '', text)                   # remove HTML tags
    text = re.sub(r'[^a-z0-9\s]', ' ', text)           # remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()            # collapse whitespace
    return text


# ─── Training Data ────────────────────────────────────────────────────────────
TRAINING_DATA = [
    # ── POSITIVE ──
    ("I absolutely love this product! It works perfectly.", "positive"),
    ("This is the best experience I have ever had.", "positive"),
    ("Amazing service and wonderful staff!", "positive"),
    ("I am so happy with the results, highly recommend!", "positive"),
    ("Excellent quality and super fast delivery.", "positive"),
    ("The food was delicious and the atmosphere was great.", "positive"),
    ("Very satisfied with my purchase. Will buy again!", "positive"),
    ("Outstanding performance, exceeded all my expectations.", "positive"),
    ("Wonderful! I couldn't be happier with this.", "positive"),
    ("Fantastic value for money, works like a charm.", "positive"),
    ("Great customer support and friendly team.", "positive"),
    ("Absolutely brilliant! Loved every bit of it.", "positive"),
    ("The movie was fantastic and kept me engaged.", "positive"),
    ("Beautiful design and very easy to use.", "positive"),
    ("Super impressed! This is exactly what I needed.", "positive"),
    ("Incredible results, far better than I expected.", "positive"),
    ("Really happy with the quality. 5 stars!", "positive"),
    ("Best product I have bought in years.", "positive"),
    ("Very good, works smoothly without any issues.", "positive"),
    ("Pleasant experience from start to finish.", "positive"),
    ("Loved it! Will definitely come back again.", "positive"),
    ("The team was professional and delivered on time.", "positive"),
    ("Superb build quality and great features.", "positive"),
    ("Highly satisfied. Would give more than 5 stars!", "positive"),
    ("Turned out better than I imagined. So grateful.", "positive"),

    # ── NEGATIVE ──
    ("This is the worst product I have ever bought.", "negative"),
    ("Terrible experience, completely disappointed.", "negative"),
    ("The service was awful and staff were rude.", "negative"),
    ("Complete waste of money. Broken on arrival.", "negative"),
    ("Very poor quality, fell apart within a week.", "negative"),
    ("Horrible! I would never recommend this to anyone.", "negative"),
    ("The app crashes constantly, completely unusable.", "negative"),
    ("Disgusting food and very slow service.", "negative"),
    ("Worst decision ever. Total scam.", "negative"),
    ("Bad quality, bad service, will not buy again.", "negative"),
    ("I regret purchasing this. Absolute garbage.", "negative"),
    ("Pathetic customer support. Never resolved my issue.", "negative"),
    ("Broken product, misleading description.", "negative"),
    ("Cheap and low quality. Very disappointing.", "negative"),
    ("Nothing worked as advertised. Total fraud.", "negative"),
    ("I am furious, this ruined my whole day.", "negative"),
    ("Extremely frustrating experience. Would not recommend.", "negative"),
    ("Delayed delivery, damaged packaging, wrong item.", "negative"),
    ("Very unhappy. The worst I have ever encountered.", "negative"),
    ("Failed miserably on every front. Awful.", "negative"),
    ("The product is defective and instructions are unclear.", "negative"),
    ("Wasted hours trying to make it work. Gave up.", "negative"),
    ("The smell was unbearable and the taste horrible.", "negative"),
    ("Do not buy this. You will regret it.", "negative"),
    ("Unacceptably bad. I feel cheated.", "negative"),

    # ── NEUTRAL ──
    ("The product arrived on time.", "neutral"),
    ("It does what it is supposed to do.", "neutral"),
    ("The package was delivered as expected.", "neutral"),
    ("Nothing special, just an average experience.", "neutral"),
    ("The item is okay, not great, not bad.", "neutral"),
    ("It works fine, but nothing remarkable.", "neutral"),
    ("Average quality, nothing to complain about.", "neutral"),
    ("Received the product, seems to work.", "neutral"),
    ("The process was straightforward.", "neutral"),
    ("Standard product, does the job.", "neutral"),
    ("It is what it is. Fairly priced.", "neutral"),
    ("Not bad, not exceptional either.", "neutral"),
    ("The results are as expected.", "neutral"),
    ("Normal delivery and normal packaging.", "neutral"),
    ("Product is functional and meets basic needs.", "neutral"),
    ("The feature set is adequate for daily use.", "neutral"),
    ("Seems decent enough for the price.", "neutral"),
    ("No complaints, but nothing outstanding.", "neutral"),
    ("Acceptable performance for the cost.", "neutral"),
    ("It gets the job done without any fuss.", "neutral"),
    ("Ordinary product, nothing stands out.", "neutral"),
    ("Moderate quality. Serves the purpose.", "neutral"),
    ("Works as described. Pretty basic.", "neutral"),
    ("Neutral on this one. Not impressed or disappointed.", "neutral"),
    ("Mediocre but passable. Would not go out of way for it.", "neutral"),
]


# ─── Train & Save ─────────────────────────────────────────────────────────────
def train_and_save_model():
    from sklearn.pipeline import Pipeline
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, accuracy_score

    os.makedirs(MODEL_DIR, exist_ok=True)

    texts  = [clean_text(t) for t, _ in TRAINING_DATA]
    labels = [l for _, l in TRAINING_DATA]

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.15, random_state=42, stratify=labels
    )

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        min_df=1,
        sublinear_tf=True,
    )

    model = LogisticRegression(
        C=1.5,
        max_iter=500,
        class_weight='balanced',
        solver='lbfgs',
    )

    # Fit
    X_train_vec = vectorizer.fit_transform(X_train)
    model.fit(X_train_vec, y_train)

    # Evaluate
    X_test_vec = vectorizer.transform(X_test)
    y_pred     = model.predict(X_test_vec)
    acc        = accuracy_score(y_test, y_pred)
    print(f"\n✅ Model trained — Accuracy: {acc * 100:.1f}%")
    print(classification_report(y_test, y_pred))

    # Save
    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(model,      MODEL_PATH)
    print(f"✅ Model saved → {MODEL_PATH}")
    print(f"✅ Vectorizer saved → {VECTORIZER_PATH}")
    return acc


# ─── Load (cached) ────────────────────────────────────────────────────────────
_model      = None
_vectorizer = None


def _load_model():
    global _model, _vectorizer
    if _model is None:
        if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
            raise FileNotFoundError(
                "Model files not found. Run: python train_model.py"
            )
        _model      = joblib.load(MODEL_PATH)
        _vectorizer = joblib.load(VECTORIZER_PATH)


# ─── Predict ──────────────────────────────────────────────────────────────────
def predict_sentiment(text: str) -> dict:
    """
    Returns:
        {
            'sentiment':      'positive' | 'negative' | 'neutral',
            'confidence':     float (0-100),
            'positive_score': float (0-100),
            'negative_score': float (0-100),
            'neutral_score':  float (0-100),
        }
    """
    _load_model()

    cleaned = clean_text(text)
    vec     = _vectorizer.transform([cleaned])
    pred    = _model.predict(vec)[0]
    proba   = _model.predict_proba(vec)[0]
    classes = list(_model.classes_)

    scores = {cls: round(float(p) * 100, 2) for cls, p in zip(classes, proba)}
    confidence = max(scores.values())

    return {
        'sentiment':      pred,
        'confidence':     round(confidence, 2),
        'positive_score': scores.get('positive', 0.0),
        'negative_score': scores.get('negative', 0.0),
        'neutral_score':  scores.get('neutral',  0.0),
    }
