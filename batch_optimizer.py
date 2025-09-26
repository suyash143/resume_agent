#!/usr/bin/env python3.10
"""
Batch ATS Resume Optimizer
Process multiple job descriptions at once
"""

import os
import json
from datetime import datetime
from ats_optimizer import analyze_job_description, inject_invisible_keywords, extract_missing_keywords_llm

def create_job_batch():
    """Create a batch of job descriptions"""
    jobs = []
    
    print("🎯 Batch ATS Resume Optimizer")
    print("=" * 40)
    print("Create a batch of job applications to optimize for")
    
    while True:
        print(f"\n📝 Job #{len(jobs) + 1}")
        company = input("Company name: ").strip()
        if not company:
            break
            
        position = input("Position title: ").strip()
        if not position:
            break
        
        print("Paste job description (press Ctrl+D when done):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            jd_text = '\n'.join(lines)
        
        jobs.append({
            'company': company,
            'position': position,
            'description': jd_text,
            'timestamp': datetime.now().isoformat()
        })
        
        print(f"✅ Added: {company} - {position}")
        
        if input("\nAdd another job? (y/n): ").lower() != 'y':
            break
    
    return jobs

def save_batch(jobs, filename="job_batch.json"):
    """Save job batch to file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    print(f"✅ Batch saved to {filename}")

def load_batch(filename="job_batch.json"):
    """Load job batch from file"""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def select_strategy():
    print("\nKeyword Extraction Strategy:")
    print("1. Default (spaCy-based, current)")
    print("2. LLM-based (extract only missing, important keywords)")
    choice = input("Select strategy (1-2, default 1): ").strip()
    if choice == "2":
        return "llm-keyword-inject"
    return "default"

def process_batch(jobs, resume_file, strategy="default"):
    """Process all jobs in batch"""
    if not jobs:
        print("❌ No jobs to process!")
        return
    
    print(f"\n🔄 Processing {len(jobs)} job applications...")
    
    # Create batch output directory
    batch_dir = f"batch_optimized_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(batch_dir, exist_ok=True)
    
    results = []
    
    # Read resume text once if LLM strategy
    resume_text = None
    if strategy == "llm-keyword-inject":
        import docx
        doc = docx.Document(resume_file)
        resume_text = "\n".join([p.text for p in doc.paragraphs])
    
    for i, job in enumerate(jobs, 1):
        print(f"\n📋 Processing {i}/{len(jobs)}: {job['company']} - {job['position']}")
        
        try:
            if strategy == "llm-keyword-inject":
                keywords = extract_missing_keywords_llm(job['description'], resume_text)
                print(f"   🔑 LLM-extracted missing keywords: {', '.join(keywords[:10])}")
            else:
                keywords = analyze_job_description(job['description'])
            
            # Create job-specific output files
            safe_company = "".join(c for c in job['company'] if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_position = "".join(c for c in job['position'] if c.isalnum() or c in (' ', '-', '_')).strip()
            
            job_dir = f"{batch_dir}/{safe_company}_{safe_position}".replace(' ', '_')
            os.makedirs(job_dir, exist_ok=True)
            
            base_name = os.path.splitext(resume_file)[0]
            output_docx = f"{job_dir}/{base_name}_ATS_Optimized.docx"
            output_pdf = f"{job_dir}/{base_name}_ATS_Optimized.pdf"
            
            # Process resume
            success = inject_invisible_keywords(resume_file, keywords, output_docx, output_pdf)
            
            # Save job description for reference
            with open(f"{job_dir}/job_description.txt", 'w', encoding='utf-8') as f:
                f.write(job['description'])
            
            # Save keywords for reference
            with open(f"{job_dir}/extracted_keywords.txt", 'w', encoding='utf-8') as f:
                f.write('\n'.join(keywords))
            
            results.append({
                'company': job['company'],
                'position': job['position'],
                'success': success,
                'keywords_count': len(keywords),
                'output_dir': job_dir
            })
            
            if success:
                print(f"   ✅ Success - {len(keywords)} keywords embedded")
            else:
                print(f"   ❌ Failed to process")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                'company': job['company'],
                'position': job['position'],
                'success': False,
                'error': str(e)
            })
    
    # Save batch results
    with open(f"{batch_dir}/batch_results.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Print summary
    successful = sum(1 for r in results if r['success'])
    print(f"\n🎉 Batch processing complete!")
    print(f"   ✅ Successful: {successful}/{len(jobs)}")
    print(f"   📁 Output directory: {batch_dir}")
    print(f"   📊 Results saved to: {batch_dir}/batch_results.json")

def main():
    """Main batch processing function"""
    try:
        print("🎯 Batch ATS Resume Optimizer")
        print("=" * 40)
        print("\nOptions:")
        print("1. Create new job batch")
        print("2. Load existing batch")
        print("3. Process existing job_batch.json")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            jobs = create_job_batch()
            if jobs:
                save_batch(jobs)
        elif choice == "2":
            filename = input("Enter batch file name (default: job_batch.json): ").strip()
            if not filename:
                filename = "job_batch.json"
            jobs = load_batch(filename)
        elif choice == "3":
            jobs = load_batch()
        else:
            print("❌ Invalid option!")
            return
        
        if not jobs:
            print("❌ No jobs found!")
            return
        
        print(f"\n📋 Found {len(jobs)} jobs:")
        for i, job in enumerate(jobs, 1):
            print(f"   {i}. {job['company']} - {job['position']}")
        
        # Select resume file
        docx_files = [f for f in os.listdir('.') if f.endswith('.docx')]
        if not docx_files:
            print("❌ No .docx files found!")
            return
        
        if len(docx_files) == 1:
            resume_file = docx_files[0]
            print(f"\n📄 Using resume: {resume_file}")
        else:
            print("\n📄 Available resume files:")
            for i, file in enumerate(docx_files, 1):
                print(f"{i}. {file}")
            
            try:
                choice = int(input("\nSelect resume file: ")) - 1
                resume_file = docx_files[choice]
            except (ValueError, IndexError):
                print("❌ Invalid selection!")
                return
        
        # Process batch
        if input(f"\nProcess {len(jobs)} jobs with {resume_file}? (y/n): ").lower().startswith('y'):
            strategy = select_strategy()
            process_batch(jobs, resume_file, strategy)
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()