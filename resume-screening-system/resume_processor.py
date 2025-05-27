import PyPDF2
import docx
import spacy
from sentence_transformers import SentenceTransformer, util
from langdetect import detect
from detoxify import Detoxify
import os
import re

# Load NLP models
nlp = spacy.load('en_core_web_sm')
model = SentenceTransformer('all-MiniLM-L6-v2')  # Lighter model for faster processing
bias_detector = Detoxify('original')

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
    return clean_text(text)

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = ' '.join([para.text for para in doc.paragraphs])
    return clean_text(text)

def extract_text_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return clean_text(text)

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text.strip()

def parse_resume(text):
    doc = nlp(text)
    skills = []
    education = []
    experience = []
    
    # Simple rule-based extraction (can be enhanced with custom NER)
    for sent in doc.sents:
        if any(keyword in sent.text.lower() for keyword in ['skill', 'skills', 'technical', 'proficiency']):
            skills.extend([token.text for token in sent if token.pos_ in ['NOUN', 'PROPN']])
        if any(keyword in sent.text.lower() for keyword in ['education', 'degree', 'university']):
            education.append(sent.text)
        if any(keyword in sent.text.lower() for keyword in ['experience', 'worked', 'employed']):
            experience.append(sent.text)
    
    return {'skills': list(set(skills)), 'education': education, 'experience': experience}

def detect_soft_skills(text):
    soft_skills = ['leadership', 'communication', 'teamwork', 'problem-solving']
    detected = []
    for skill in soft_skills:
        if skill in text.lower():
            detected.append(skill)
    return detected, len(detected) / len(soft_skills)  # Soft skill score

def detect_bias(text):
    results = bias_detector.predict(text)
    return 'Potential bias detected' if results['toxicity'] > 0.7 else 'No bias detected'

def process_resumes(job_desc_path, resume_paths):
    # Extract job description based on file extension
    if job_desc_path.endswith('.pdf'):
        job_desc_text = extract_text_from_pdf(job_desc_path)
    elif job_desc_path.endswith('.docx'):
        job_desc_text = extract_text_from_docx(job_desc_path)
    elif job_desc_path.endswith('.txt'):
        job_desc_text = extract_text_from_txt(job_desc_path)
    else:
        raise ValueError(f"Unsupported job description file format: {job_desc_path}")
    
    job_desc_embedding = model.encode(job_desc_text)
    
    results = []
    for resume_path in resume_paths:
        # Extract resume text
        resume_text = extract_text_from_pdf(resume_path) if resume_path.endswith('.pdf') else extract_text_from_docx(resume_path)
        
        # Parse resume
        resume_data = parse_resume(resume_text)
        
        # Semantic matching
        resume_embedding = model.encode(resume_text)
        match_score = float(util.cos_sim(job_desc_embedding, resume_embedding)[0][0])
        # Scale match_score from 0–1 to 0–100
        match_score = match_score * 100
        
        # Skill gap analysis
        job_skills = set(parse_resume(job_desc_text)['skills'])
        resume_skills = set(resume_data['skills'])
        missing_skills = list(job_skills - resume_skills)
        
        # Soft skill detection
        soft_skills, soft_skill_score = detect_soft_skills(resume_text)
        
        # Bias detection
        bias_warning = detect_bias(resume_text)
        
        # Highlight skills in resume text
        highlighted_text = resume_text
        for skill in resume_skills:
            highlighted_text = highlighted_text.replace(skill, f'<span class="highlight-match">{skill}</span>')
        for skill in missing_skills:
            highlighted_text = highlighted_text.replace(skill, f'<span class="highlight-missing">{skill}</span>')
        
        results.append({
            'filename': os.path.basename(resume_path),
            'match_score': round(match_score, 2),  # Round to 2 decimal places
            'skills': ','.join(resume_skills) if resume_skills else 'None',
            'missing_skills': ','.join(missing_skills) if missing_skills else 'None',
            'soft_skills': ','.join(soft_skills) if soft_skills else 'None',
            'soft_skill_score': round(soft_skill_score, 2),
            'bias_warning': bias_warning,
            'highlighted_resume': highlighted_text
        })
    
    # Sort by match score and limit to top 10
    results = sorted(results, key=lambda x: x['match_score'], reverse=True)[:10]
    
    return results