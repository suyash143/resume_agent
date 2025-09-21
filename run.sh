#!/bin/bash

echo "🚀 Smart ATS Resume Optimizer Setup"
echo "===================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment with Python 3.10..."
    python3.10 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install required packages
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Download spaCy model
echo "🧠 Downloading spaCy language model..."
python3.10 -m spacy download en_core_web_sm

echo ""
echo "✅ Setup complete! Choose an option:"
echo ""
echo "1. Quick optimize (uses job_description.txt)"
echo "2. Interactive CLI"
echo "3. Batch processor"
echo ""

read -p "Select option (1-3): " choice

case $choice in
    1)
        echo "🔄 Running quick optimization..."
        python3.10 ats_optimizer.py
        ;;
    2)
        echo "🎯 Starting interactive CLI..."
        python3.10 ats_cli.py
        ;;
    3)
        echo "📋 Starting batch processor..."
        python3.10 batch_optimizer.py
        ;;
    *)
        echo "❌ Invalid option. Running default optimizer..."
        python3.10 ats_optimizer.py
        ;;
esac

echo ""
echo "🎉 Done! Check the output files."

