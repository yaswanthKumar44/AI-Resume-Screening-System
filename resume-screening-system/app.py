from flask import Flask, request, render_template, send_file
from resume_processor import process_resumes
import os
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
REPORT_FOLDER = 'reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORT_FOLDER'] = REPORT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        job_desc_text = request.form.get('job_description_text')
        job_desc_file = request.files.get('job_description_file')
        resume_files = request.files.getlist('resumes')
        
        # Handle job description (text or file)
        if job_desc_text:
            job_desc_path = os.path.join(app.config['UPLOAD_FOLDER'], 'job_description.txt')
            with open(job_desc_path, 'w', encoding='utf-8') as f:
                f.write(job_desc_text)
        elif job_desc_file and job_desc_file.filename:
            job_desc_path = os.path.join(app.config['UPLOAD_FOLDER'], job_desc_file.filename)
            job_desc_file.save(job_desc_path)
        else:
            return render_template('index.html', error="Please provide a job description (text or file).")
        
        # Save resumes
        resume_paths = []
        for resume in resume_files:
            if resume.filename:
                resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
                resume.save(resume_path)
                resume_paths.append(resume_path)
        
        if not resume_paths:
            return render_template('index.html', error="Please upload at least one resume.")
        
        # Process resumes (returns top 10)
        results = process_resumes(job_desc_path, resume_paths)
        
        # Save top 10 to CSV (exclude highlighted_resume)
        report_path = os.path.join(app.config['REPORT_FOLDER'], 'candidate_report.csv')
        results_df = pd.DataFrame(results)
        results_df = results_df[['filename', 'match_score', 'skills', 'missing_skills', 'soft_skills', 'soft_skill_score', 'bias_warning']]
        results_df.insert(0, 'rank', range(1, len(results_df) + 1))  # Add rank column
        results_df.to_csv(report_path, index=False, encoding='utf-8')
        
        return render_template('results.html', results=results, report_path=report_path)
    except Exception as e:
        return render_template('index.html', error=f"An error occurred: {str(e)}")

@app.route('/download/<filename>')
def download_report(filename):
    try:
        return send_file(os.path.join(app.config['REPORT_FOLDER'], filename), as_attachment=True)
    except FileNotFoundError:
        return render_template('index.html', error="Report not found. Please process resumes first.")

if __name__ == '__main__':
    app.run(debug=True)