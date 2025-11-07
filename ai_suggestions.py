import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("")

def suggest_improvements(parsed_resume: dict, job_text: str) -> str:
    """Provide AI-based or rule-based resume suggestions."""
    if not openai.api_key:
        # fallback if no API key
        missing = []
        for skill in ["python", "aws", "docker", "machine learning", "sql", "nlp", "react", "excel"]:
            if skill not in [s.lower() for s in parsed_resume.get("skills", [])]:
                if skill.lower() in job_text.lower():
                    missing.append(skill)
        if not missing:
            return "✅ Resume aligns well with job requirements."
        return f"Consider adding or highlighting: {', '.join(missing)}"

    # use OpenAI model
    prompt = f"""
    You are an expert resume coach. Given the candidate's resume details and the job description,
    suggest improvements in concise bullet points.

    Resume:
    Name: {parsed_resume.get('name')}
    Skills: {', '.join(parsed_resume.get('skills', []))}
    Education: {', '.join(parsed_resume.get('education', []))}
    Experience: {', '.join(parsed_resume.get('experience', []))}

    Job Description:
    {job_text}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=250
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling OpenAI API: {e}"
