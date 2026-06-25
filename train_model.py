#!/usr/bin/env python3
"""
train_model.py
==============
Run this ONCE before starting the Django server to train and save the
Sentiment Analysis ML model.

Usage:
    python train_model.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentiment_project.settings')

from sentiment.ml_model import train_and_save_model

if __name__ == '__main__':
    print("=" * 55)
    print("  Smart Sentiment Analysis System — Model Trainer")
    print("=" * 55)
    print("\n🔄 Training model, please wait...\n")
    acc = train_and_save_model()
    print(f"\n✅ Done! Model is ready. Accuracy: {acc * 100:.1f}%")
    print("   You can now start the Django server.\n")
