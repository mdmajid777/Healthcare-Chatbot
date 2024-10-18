import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to load questions and answers from CSV
def load_qa_data():
    try:
        df = pd.read_csv('healthcare_qa.csv')
        return df
    except FileNotFoundError:
        st.error("CSV file not found. Please make sure 'healthcare_qa.csv' is in the same directory as this script.")
        return pd.DataFrame(columns=['Question', 'Answer'])

# Function to create CSV if it doesn't exist
def create_csv():
    healthcare_qa = [
        ("What are the symptoms of COVID-19?", "Common symptoms include fever, cough, and difficulty breathing.","what is chest pain"),
        ("What is chest pain", "Chest pain is discomfort or pain in the chest area, often caused by heart, lung, or muscle-related issues."),
        ("How often should I get a physical exam?", "Generally, adults should get a physical exam every 1-3 years, depending on age and health status."),
        ("What is the recommended daily water intake?", "The general recommendation is about 8 cups (64 ounces) of water per day."),
        ("How can I lower my cholesterol?", "Eat a heart-healthy diet, exercise regularly, maintain a healthy weight, and avoid smoking."),
        ("What are the early signs of diabetes?", "Common signs include increased thirst, frequent urination, unexplained weight loss, and fatigue."),
        ("How can I improve my sleep hygiene?", "Maintain a regular sleep schedule, create a relaxing bedtime routine, and avoid screens before bed."),
        ("What are the benefits of regular exercise?", "Regular exercise can improve cardiovascular health, strengthen muscles and bones, and boost mental health."),
        ("How can I reduce stress?", "Practice relaxation techniques, exercise regularly, get enough sleep, and maintain a healthy work-life balance."),
        ("What is the importance of vaccination?", "Vaccinations protect against serious diseases and help prevent the spread of infections in communities."),
        ("How can I maintain a healthy diet?", "Eat a variety of fruits, vegetables, whole grains, lean proteins, and healthy fats. Limit processed foods and added sugars."),
        # ... (include the rest of the original 100 questions and answers here)
        ("What are the signs of a healthy thyroid function?", "Signs include stable weight, regular heartbeat, good energy levels, and normal body temperature."),
        
        # Adding 50 more healthcare-related questions and answers
        ("What is the purpose of vitamin D?", "Vitamin D helps the body absorb calcium, promotes bone growth, and supports immune function."),
        ("How can I prevent food poisoning?", "Practice good hygiene, cook foods thoroughly, store foods properly, and avoid cross-contamination."),
        ("What are the benefits of meditation?", "Meditation can reduce stress, improve focus, enhance emotional well-being, and promote better sleep."),
        ("How can I improve my posture?", "Be mindful of your posture, strengthen core muscles, use ergonomic furniture, and take regular breaks from sitting."),
        ("What are the symptoms of anemia?", "Common symptoms include fatigue, weakness, pale skin, shortness of breath, and dizziness."),
        ("How can I boost my metabolism?", "Exercise regularly, build muscle mass, stay hydrated, get enough sleep, and eat protein-rich foods."),
        ("What are the benefits of probiotics?", "Probiotics can improve digestive health, boost immune function, and potentially help with weight management."),
        ("How can I prevent osteoporosis?", "Consume adequate calcium and vitamin D, exercise regularly, avoid smoking, and limit alcohol consumption."),
        ("What are the signs of heat exhaustion?", "Signs include heavy sweating, dizziness, headache, nausea, and cool, moist skin with goosebumps."),
        ("How can I manage seasonal allergies?", "Avoid allergens when possible, use air filters, take over-the-counter antihistamines, and consider immunotherapy."),
        ("What are the benefits of intermittent fasting?", "Potential benefits include weight loss, improved insulin sensitivity, and increased longevity."),
        ("How can I improve my flexibility?", "Practice stretching exercises regularly, try yoga or Pilates, and maintain proper hydration."),
        ("What are the signs of a concussion?", "Signs include headache, confusion, dizziness, nausea, and sensitivity to light or noise."),
        ("How can I prevent eye strain from digital devices?", "Follow the 20-20-20 rule, adjust screen brightness, use proper lighting, and consider blue light filters."),
        ("What are the benefits of omega-3 fatty acids?", "Omega-3s can reduce inflammation, lower heart disease risk, and support brain health."),
        ("How can I manage chronic pain?", "Use pain medications as directed, try physical therapy, practice relaxation techniques, and maintain a healthy lifestyle."),
        ("What are the symptoms of gallstones?", "Symptoms may include sudden pain in the upper right abdomen, nausea, and vomiting."),
        ("How can I improve my lung capacity?", "Practice deep breathing exercises, engage in cardiovascular activities, and avoid smoking."),
        ("What are the benefits of cold water therapy?", "Cold water therapy may reduce inflammation, improve circulation, and boost mood and energy levels."),
        ("How can I prevent kidney stones?", "Stay hydrated, limit sodium intake, eat calcium-rich foods, and avoid excessive animal protein."),
        ("What are the signs of hypothyroidism?", "Signs include fatigue, weight gain, cold sensitivity, dry skin, and depression."),
        ("How can I improve my gut health?", "Eat a diverse range of foods, consume fermented foods, limit artificial sweeteners, and stay hydrated."),
        ("What are the benefits of high-intensity interval training (HIIT)?", "HIIT can improve cardiovascular fitness, burn more calories, and increase metabolic rate."),
        ("How can I manage eczema?", "Keep skin moisturized, identify and avoid triggers, use gentle skincare products, and manage stress."),
        ("What are the symptoms of celiac disease?", "Symptoms may include digestive issues, fatigue, skin rash, and unexplained weight loss."),
        ("How can I improve my balance?", "Practice balance exercises, try yoga or tai chi, and strengthen your core muscles."),
        ("What are the benefits of vitamin C?", "Vitamin C supports immune function, acts as an antioxidant, and aids in collagen production."),
        ("How can I prevent carpal tunnel syndrome?", "Use proper ergonomics, take regular breaks, stretch your hands and wrists, and maintain good posture."),
        ("What are the signs of iron deficiency?", "Signs include fatigue, weakness, pale skin, shortness of breath, and brittle nails."),
        ("How can I manage high blood pressure naturally?", "Reduce sodium intake, exercise regularly, manage stress, maintain a healthy weight, and limit alcohol."),
        ("What are the benefits of resistance training?", "Resistance training can build muscle mass, increase bone density, boost metabolism, and improve overall strength."),
        ("How can I improve my memory?", "Get enough sleep, exercise regularly, eat a healthy diet, stay mentally active, and manage stress."),
        ("What are the symptoms of lupus?", "Symptoms may include fatigue, joint pain, skin rashes, and fever."),
        ("How can I prevent cavities?", "Brush twice daily, floss regularly, limit sugary foods, use fluoride toothpaste, and visit your dentist regularly."),
        ("What are the benefits of mindfulness?", "Mindfulness can reduce stress, improve focus, enhance emotional regulation, and promote overall well-being."),
        ("How can I manage arthritis pain?", "Exercise regularly, maintain a healthy weight, use hot and cold therapy, and consider medications or supplements."),
        ("What are the signs of a migraine?", "Signs may include intense headache, sensitivity to light and sound, nausea, and visual disturbances."),
        ("How can I improve my cardiovascular endurance?", "Engage in regular aerobic exercise, gradually increase intensity and duration, and stay consistent."),
        ("What are the benefits of getting enough sleep?", "Adequate sleep can improve memory, mood, immune function, and overall physical and mental health."),
        ("How can I prevent lower back pain?", "Maintain good posture, exercise regularly, use proper lifting techniques, and ensure your workspace is ergonomic."),
        ("What are the symptoms of pneumonia?", "Symptoms may include cough, fever, chills, shortness of breath, and chest pain."),
        ("How can I manage stress at work?", "Take regular breaks, prioritize tasks, practice time management, and maintain a healthy work-life balance."),
        ("What are the benefits of eating whole grains?", "Whole grains provide fiber, vitamins, minerals, and can help reduce the risk of heart disease and diabetes."),
        ("How can I improve my digestion?", "Eat slowly, stay hydrated, exercise regularly, manage stress, and consider adding probiotics to your diet."),
        ("What are the signs of a healthy immune system?", "Signs include rarely getting sick, quick recovery from illnesses, and having lots of energy."),
        ("How can I prevent age-related cognitive decline?", "Stay mentally active, exercise regularly, maintain social connections, and eat a healthy diet."),
        ("What are the benefits of yoga?", "Yoga can improve flexibility, strength, balance, reduce stress, and promote overall physical and mental well-being.")
    ]
    
    df = pd.DataFrame(healthcare_qa, columns=['Question', 'Answer'])
    df.to_csv('healthcare_qa.csv', index=False)
    return df

# Function to find the most similar question and return its answer
def get_answer(user_question, qa_df, vectorizer, question_vectors):
    user_vector = vectorizer.transform([user_question])
    similarities = cosine_similarity(user_vector, question_vectors)
    most_similar_idx = similarities.argmax()
    return qa_df.iloc[most_similar_idx]['Answer']

# Streamlit app
def main():
    st.title("Healthcare Chatbot")

    # Load or create Q&A data
    qa_df = load_qa_data()
    if qa_df.empty:
        qa_df = create_csv()
        st.success("Created 'healthcare_qa.csv' with 150 questions and answers.")

    # Prepare vectorizer and question vectors
    vectorizer = TfidfVectorizer()
    question_vectors = vectorizer.fit_transform(qa_df['Question'])

    # User input for question
    user_question = st.text_input("Ask a healthcare-related question:")

    if user_question:
        answer = get_answer(user_question, qa_df, vectorizer, question_vectors)
        st.write("Answer:")
        st.write(answer)

    # Display total number of questions
    # st.sidebar.write(f"Total number of questions in database: {len(qa_df)}")

if __name__ == "__main__":
    main()