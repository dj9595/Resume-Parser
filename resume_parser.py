import re
import json

def parse_resume(resume_text):
    resume = {}
    
    # Parsing name
    name_match = re.search(r'Name:\s*(.*)', resume_text)
    if name_match:
        resume['name'] = name_match.group(1)
    
    # Parsing email
    email_match = re.search(r'Email:\s*(.*)', resume_text)
    if email_match:
        resume['email'] = email_match.group(1)
    
    # Parsing phone
    phone_match = re.search(r'Phone:\s*(.*)', resume_text)
    if phone_match:
        resume['phone'] = phone_match.group(1)
    
    # Parsing experience
    experience = []
    exp_matches = re.findall(r'(\d+)\.\s*(.*?)\s*at\s*(.*?)\s*\((.*?)\)\s*(-.*?)(?=\d+\.|$)', resume_text, re.DOTALL)
    for match in exp_matches:
        experience.append({
            'position': match[1].strip(),
            'company': match[2].strip(),
            'duration': match[3].strip(),
            'responsibilities': [resp.strip() for resp in match[4].split('-') if resp.strip()]
        })
    resume['experience'] = experience
    
    # Parsing education
    education = []
    edu_matches = re.findall(r'-\s*(.*?)\s*,\s*(.*?)\s*\((.*?)\)\s*(-.*?)(?=-\s*|$)', resume_text, re.DOTALL)
    for match in edu_matches:
        education.append({
            'degree': match[1].strip(),
            'institution': match[0].strip(),
            'duration': match[2].strip(),
            'details': match[3].strip().split(', ')
        })
    resume['education'] = education
    
    # Parsing skills
    skills_match = re.search(r'Skills:\s*(-.*?)(?=Projects:|$)', resume_text, re.DOTALL)
    if skills_match:
        skills = [skill.strip() for skill in skills_match.group(1).split('-') if skill.strip()]
        resume['skills'] = skills
    
    # Parsing projects
    projects = []
    proj_matches = re.findall(r'(\d+)\.\s*(.*?)(?=1\.|$)', resume_text, re.DOTALL)
    for match in proj_matches:
        proj_details = match[1].strip().split('\n')
        projects.append({
            'title': proj_details[0].strip(),
            'description': ' '.join(proj_details[1:]).strip()
        })
    resume['projects'] = projects
    
    return json.dumps(resume, indent=4)

# Example resume text
resume_text = """
Name: John Doe
Email: john.doe@example.com
Phone: +1234567890

Experience:
1. Software Engineer at XYZ Corp (Jan 2020 - Present)
   - Developed web applications using JavaScript, React, and Node.js.
   - Collaborated with cross-functional teams to define project requirements and deliverables.
   - Improved application performance by 30% through optimization techniques.

2. Junior Developer at ABC Inc (Jun 2018 - Dec 2019)
   - Assisted in developing internal tools using Python and Django.
   - Wrote unit tests to ensure code quality and reliability.
   - Participated in code reviews and team meetings.

Education:
- BSc in Computer Science, University of Somewhere (2014 - 2018)
  - Relevant coursework: Data Structures, Algorithms, Database Systems, Machine Learning

Skills:
- Programming Languages: JavaScript, Python, Java
- Web Technologies: HTML, CSS, React, Node.js
- Tools: Git, Docker, Jenkins

Projects:
1. E-commerce Website
   - Developed a full-stack e-commerce website using React and Node.js.
   - Implemented user authentication, product management, and payment processing.

2. Machine Learning Model for Predictive Analytics
   - Built and trained a machine learning model using Python and scikit-learn.
   - Deployed the model as a REST API for integration with other applications.
"""

parsed_resume = parse_resume(resume_text)
print(parsed_resume)
