# llm_prompt.py

LLM_KEYWORD_EXTRACTION_PROMPT = '''You are an ATS (Applicant Tracking System) keyword extraction expert. Your goal is to help candidates pass ATS screening filters.

JOB DESCRIPTION:
{jd_text}

CURRENT RESUME CONTENT:
{resume_text}

TASK: Extract ONLY the critical keywords from the job description that are missing from the resume and are likely to be used by ATS systems for filtering candidates.

FOCUS ON THESE ATS-CRITICAL CATEGORIES:
1. **Technical Skills & Tools**: Programming languages, frameworks, software, platforms, databases
2. **Certifications & Qualifications**: Required certifications, degrees, licenses
3. **Industry Buzzwords**: Specific methodologies, processes, industry-standard terms
4. **Job Title Variations**: Alternative titles for the same role
5. **Required Experience**: Specific years of experience, seniority levels
6. **Hard Requirements**: Must-have qualifications explicitly mentioned
7. **Action Verbs**: Key verbs that describe required activities (develop, implement, manage, etc.)
8. **Compliance & Standards**: Industry regulations, security clearances, compliance frameworks

EXTRACTION RULES:
- Extract keywords that ATS systems typically scan for (exact matches, not synonyms)
- Prioritize exact phrases and technical terms over generic words
- Include both singular and plural forms if both appear in job description
- Focus on "must-have" vs "nice-to-have" requirements
- Include acronyms AND their full forms (e.g., "AI, Artificial Intelligence")
- Extract specific software versions if mentioned (e.g., "Python 3.x", "AWS Lambda")

EXCLUSION RULES:
- Skip keywords already present in the resume (case-insensitive check)
- Ignore generic soft skills unless specifically emphasized
- Skip company-specific terms that won't help with other applications
- Avoid overly broad terms like "good", "strong", "excellent"

OUTPUT FORMAT: Return ONLY a comma-separated list of missing keywords, no explanations or additional text  but ordered in descending order, starting from high priority keywords to lesser priority one ..

KEYWORDS:'''

