#!/usr/bin/env python3.10
"""
Smart ATS Resume Optimizer CLI
Interactive command-line interface for optimizing resumes
"""

import os
import sys
from ats_optimizer import analyze_job_description, inject_invisible_keywords, extract_smart_keywords, extract_missing_keywords_llm

def get_user_input():
    """Get job description from user input"""
    print("🎯 Smart ATS Resume Optimizer")
    print("=" * 40)
    print("\nOptions:")
    print("1. Use existing job_description.txt file")
    print("2. Paste job description directly")
    print("3. Load from custom file")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        if os.path.exists("job_description.txt"):
            with open("job_description.txt", "r", encoding='utf-8') as f:
                return f.read()
        else:
            print("❌ job_description.txt not found!")
            return None
    
    elif choice == "2":
        print("\n📝 Paste the job description below (press Ctrl+D when done):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            return '\n'.join(lines)
    
    elif choice == "3":
        filepath = input("Enter file path: ").strip()
        if os.path.exists(filepath):
            with open(filepath, "r", encoding='utf-8') as f:
                return f.read()
        else:
            print(f"❌ File not found: {filepath}")
            return None
    
    else:
        print("❌ Invalid option!")
        return None

def select_resume():
    """Let user select resume file"""
    docx_files = [f for f in os.listdir('.') if f.endswith('.docx')]
    
    if not docx_files:
        print("❌ No .docx files found in current directory!")
        return None
    
    if len(docx_files) == 1:
        print(f"📄 Using resume: {docx_files[0]}")
        return docx_files[0]
    
    print("\n📄 Available resume files:")
    for i, file in enumerate(docx_files, 1):
        print(f"{i}. {file}")
    
    try:
        choice = int(input("\nSelect resume file: ")) - 1
        if 0 <= choice < len(docx_files):
            return docx_files[choice]
        else:
            print("❌ Invalid selection!")
            return None
    except ValueError:
        print("❌ Please enter a number!")
        return None

def select_strategy():
    """Select keyword extraction strategy"""
    print("\nKeyword Extraction Strategy:")
    print("1. Default (spaCy-based, current)")
    print("2. LLM-based (extract only missing, important keywords)")
    choice = input("Select strategy (1-2, default 1): ").strip()
    if choice == "2":
        return "llm-keyword-inject"
    return "default"

def main():
    """Main CLI function"""
    try:
        # Get job description
        jd_text = get_user_input()
        if not jd_text:
            return
        
        # Save job description for future use
        with open("job_description.txt", "w", encoding='utf-8') as f:
            f.write(jd_text)
        print("✅ Job description saved to job_description.txt")
        
        # Select resume
        resume_file = select_resume()
        if not resume_file:
            return
        
        # Select strategy
        strategy = select_strategy()
        
        # Configure output
        output_dir = "optimized_resume"
        base_name = os.path.splitext(resume_file)[0]
        output_docx = f"{output_dir}/{base_name}_ATS_Optimized.docx"
        output_pdf = f"{output_dir}/{base_name}_ATS_Optimized.pdf"
        
        # Ask about PDF generation
        generate_pdf = input("\n📄 Generate PDF version? (y/n): ").lower().startswith('y')
        
        # Extract keywords based on strategy
        if strategy == "llm-keyword-inject":
            with open(resume_file, "rb") as f:
                import docx
                doc = docx.Document(f)
                resume_text = "\n".join([p.text for p in doc.paragraphs])
            keywords = extract_missing_keywords_llm(jd_text, resume_text)
            print(f"\n🔑 LLM-extracted missing keywords: {', '.join(keywords[:10])}")
        else:
            keywords = analyze_job_description(jd_text)
        
        # Process resume
        print(f"\n🔄 Processing resume: {resume_file}")
        success = inject_invisible_keywords(
            resume_file, 
            keywords, 
            output_docx, 
            output_pdf if generate_pdf else None
        )
        
        if success:
            print(f"\n🎉 Optimization complete!")
            print(f"\n📁 Output files:")
            print(f"   📄 DOCX: {output_docx}")
            if generate_pdf:
                print(f"   📄 PDF: {output_pdf}")
            
            print(f"\n💡 Next steps:")
            print(f"   • Test with ATS scanners online")
            print(f"   • Use DOCX for online applications")
            print(f"   • Use PDF for email submissions")
            print(f"   • Keywords are completely invisible to humans")
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()