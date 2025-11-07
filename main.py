import os
from resume_parser import parse_resume
from resume_ranker import rank_resume
from ai_suggestions import suggest_improvements

DATA_DIR = "data"
JOBS_DIR = "job_descriptions"

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def process_all():
    job_files = [os.path.join(JOBS_DIR, f) for f in os.listdir(JOBS_DIR) if f.endswith(".txt")]
    resume_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith((".pdf", ".txt"))]

    print(f"Found {len(resume_files)} resumes and {len(job_files)} job descriptions.\n")

    for resume_path in resume_files:
        print(f"Processing resume: {os.path.basename(resume_path)}")
        parsed = parse_resume(resume_path)
        resume_text = parsed["raw_text"]

        for job_path in job_files:
            job_text = load_text(job_path)
            score = rank_resume(resume_text, job_text)
            suggestion = suggest_improvements(parsed, job_text)

            print(f"  💼 Job: {os.path.basename(job_path)}")
            print(f"  🔹 Match Score: {score}%")
            print(f"  💡 Suggestions: {suggestion[:200]}...\n")

if __name__ == "__main__":
    process_all()
