#!/usr/bin/env python3.10
"""
Test script for ATS optimizer functionality
"""

import os
from ats_optimizer import extract_smart_keywords, analyze_job_description

def test_keyword_extraction():
    """Test keyword extraction functionality"""
    print("🧪 Testing Keyword Extraction")
    print("=" * 30)
    
    # Test with sample job description
    with open('job_description.txt', 'r') as f:
        sample_jd = f.read()
        f.close()
    
    keywords = extract_smart_keywords(sample_jd)
    
    print(f"✅ Extracted {len(keywords)} keywords")
    print(f"📋 Top 10: {', '.join(keywords[:10])}")
    
    # Test analysis function
    print(f"\n🔍 Running full analysis...")
    analyzed_keywords = analyze_job_description(sample_jd)
    
    return len(analyzed_keywords) > 0

def test_file_operations():
    """Test file operations"""
    print(f"\n🗂️  Testing File Operations")
    print("=" * 30)
    
    # Check if resume file exists
    resume_files = [f for f in os.listdir('.') if f.endswith('.docx')]
    print(f"📄 Found {len(resume_files)} DOCX files")
    
    if resume_files:
        print(f"✅ Resume files: {', '.join(resume_files)}")
        return True
    else:
        print(f"⚠️  No DOCX resume files found")
        return False

def main():
    """Run all tests"""
    print("🚀 ATS Optimizer Test Suite")
    print("=" * 40)
    
    try:
        # Test 1: Keyword extraction
        test1_passed = test_keyword_extraction()
        
        # Test 2: File operations
        test2_passed = test_file_operations()
        
        # Summary
        print(f"\n📊 Test Results")
        print("=" * 20)
        print(f"✅ Keyword Extraction: {'PASS' if test1_passed else 'FAIL'}")
        print(f"✅ File Operations: {'PASS' if test2_passed else 'FAIL'}")
        
        if test1_passed and test2_passed:
            print(f"\n🎉 All tests passed! The optimizer is ready to use.")
            print(f"\n💡 Next steps:")
            print(f"   1. Run: python3.10 ats_optimizer.py")
            print(f"   2. Or run: python3.10 ats_cli.py for interactive mode")
            print(f"   3. Or run: ./run.sh for guided setup")
        else:
            print(f"\n❌ Some tests failed. Check the setup.")
            
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()