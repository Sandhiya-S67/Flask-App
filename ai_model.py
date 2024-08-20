import google.generativeai as genai

genai.configure(api_key="AIzaSyCDo-II0-44Fuq1PKnaDo9h6w7GL3Nie9U")

model = genai.GenerativeModel('gemini-1.5-flash')

def generate_improvements(complaints, feedbacks):
    prompt = "Based on the following complaints and feedbacks, suggest improvements for the automotive features:\n"
    
    for complaint in complaints:
        prompt += f"Complaint: {complaint['complaint_text']}\n"
    
    for feedback in feedbacks:
        prompt += f"Feedback: {feedback['feedback_text']}\n"
    
    response = model.generate_content(prompt)
    
    improvements_text = response.candidates[0].content.parts[0].text
    
    formatted_text = improvements_text.replace('#', '').replace('*', '')

    return formatted_text.split('\n\n')
