# AI-Resume Screening System 🚀

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.3-blueviolet)
![License](https://img.shields.io/badge/License-MIT-green)

A powerful **AI-Resume Screening System** built to streamline the hiring process by ranking candidates based on their resumes and job descriptions. This project leverages Natural Language Processing (NLP) to analyze resumes, match skills, calculate scores, and identify potential biases — all wrapped in a modern, futuristic UI with professional animations.

This tool is designed to help recruiters efficiently filter top candidates while providing a visually stunning and user-friendly experience.

---

## ✨ Features

- **Resume Parsing**: Extracts skills, experience, and education from uploaded resumes using NLP.
- **Job Description Matching**: Compares candidate resumes against job requirements to calculate a match score.
- **Soft Skills Analysis**: Identifies and scores soft skills, providing a comprehensive candidate evaluation.
- **Bias Detection**: Flags potential biases in resumes to ensure fair screening.
- **Futuristic UI**: A sleek, dark-themed interface with glassmorphism effects, glowing badges, and neon buttons.
- **Professional Animations**: Typing effects, scale-in transitions, and slide-down animations for a polished experience.
- **Responsive Design**: Fully responsive layout, optimized for desktop and mobile devices.
- **Top Candidate Highlight**: Displays the top candidate’s resume with highlighted matches.
- **Export Results**: Download candidate rankings as a CSV report.

---

## 🎥 Demo


---

## 🛠️ Installation

Follow these steps to set up the project locally.

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yaswanthKumar44/AI-Resume-Screening-System.git
   cd ai-resume-screening-system
````

2. **Create a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Install SpaCy Language Model**:

   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Create Required Directories**:

   ```bash
   mkdir uploads reports
   ```

6. **Run the Application**:

   ```bash
   python app.py
   ```

7. **Access the App**:
   Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📖 Usage

**Upload Files**:

* On the homepage, upload a job description (text or PDF) and one or more candidate resumes (PDF format).
* Click **Submit** to process the files.

**View Results**:

* The results page displays a table of the top 10 candidates, ranked by match score.
* Columns include filename, match score, skills, missing skills, soft skills, soft skill score, and bias warnings.
* Skills and missing skills are shown as glowing badges with a “Show More” option for long lists.
* Hover over badges to see tooltips, and enjoy the futuristic animations.

**Highlighted Resume**:

* The top candidate’s resume is displayed below the table with highlighted matches.

**Download Report**:

* Click **Download Report** to export the candidate rankings as a CSV file.

**Return to Upload**:

* Click **Back to Upload** to screen a new set of candidates.

---

## ⚙️ Technologies Used

### Backend:

* Python 3.9+
* Flask (Web Framework)
* SpaCy (NLP for resume parsing)
* NLTK (Text processing)
* PyMuPDF (PDF parsing)

### Frontend:

* HTML5, CSS3, JavaScript
* Bootstrap 5.3.3 (Responsive design)
* Font Awesome 6.5.2 (Icons)
* Google Fonts (Inter and Orbitron for futuristic typography)

### Styling & Animations:

* Glassmorphism effects with backdrop-filter
* Glowing badges and neon buttons
* Custom animations (typing, scale-in, slide-down, pop-in)

---

## 📁 Project Structure

```
ai-resume-screening-system/
│
├── app.py                    # Main Flask application
├── requirements.txt          # Project dependencies
├── resume_processor.py       # Logic for resume parsing and scoring
├── templates/
│   ├── index.html            # Upload page
│   ├── results.html          # Results page with futuristic UI
├── static/
│   ├── style.css             # Global styles
├── uploads/                  # Directory for uploaded files
└── reports/                  # Directory for exported CSV reports
```

---


## 📬 Contact

For questions, feedback, or collaboration, reach out to [yashyaswanth714l@gmail.com]

---

## ⭐ Acknowledgements

Built with ❤️ by P.Yaswanth Kumar

