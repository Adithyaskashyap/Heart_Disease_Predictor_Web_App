from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import google.generativeai as genai
import os


app = Flask(__name__)




GEMINI_API_KEY = "AIzaSyCEq1MU8DvpMMQg8TmAtFid4yhHgVo9U1E"

genai.configure(api_key=GEMINI_API_KEY)

chat_model = genai.GenerativeModel('gemini-2.5-flash')



dt_model = pickle.load(open('models/DecisionTree1.pkl', 'rb'))

lr_model = pickle.load(open('models/LogisticRegresion.pkl', 'rb'))

svm_model = pickle.load(open('models/Svm.pkl', 'rb'))



@app.route('/')
def home():
    return render_template('index.html')



@app.route('/decision-tree')
def decision_tree_page():
    return render_template('decision_tree.html')



@app.route('/logistic-regression')
def logistic_page():
    return render_template('LogisticRegression.html')



@app.route('/svm')
def svm_page():
    return render_template('svm.html')



@app.route('/know_about')
def know_heart():
    return render_template('know_about.html')



@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')



def preprocess(data):

    sex = 1 if data['sex'] == 'Male' else 0

    chest_pain = [
        'Typical Angina',
        'Atypical Angina',
        'Non-Anginal Pain',
        'Asymptomatic'
    ].index(data['chest_pain'])

    fastingbs = 1 if data['fastingbs'] == '>120' else 0

    resting_ecg = [
        'Left Ventricular Hypertrophy',
        'Normal',
        'ST-T Wave Abnormalities'
    ].index(data['resting_ecg'])

    exercise_angina = 1 if data['exercise_angina'] == 'Yes' else 0

    st_slope = [
        'DownSloping',
        'Flat',
        'Upsloping'
    ].index(data['st_slope'])

    input_df = pd.DataFrame({

        'Age': [int(data['age'])],

        'Sex': [sex],

        'ChestPainType': [chest_pain],

        'RestingBP': [int(data['resting_bp'])],

        'Cholesterol': [float(data['cholesterol'])],

        'FastingBS': [fastingbs],

        'RestingECG': [resting_ecg],

        'MaxHR': [int(data['max_hr'])],

        'ExerciseAngina': [exercise_angina],

        'Oldpeak': [float(data['oldpeak'])],

        'ST_Slope': [st_slope]

    })

    return input_df



@app.route('/api/predict/dt', methods=['POST'])

def predict_dt():

    data = request.json

    processed_data = preprocess(data)

    prediction = dt_model.predict(processed_data)[0]

    result = (
        "Has Heart Disease"
        if prediction == 1
        else "No Heart Disease"
    )

    return jsonify({
        'model': 'Decision Tree',
        'prediction': result
    })



@app.route('/api/predict/lr', methods=['POST'])

def predict_lr():

    data = request.json

    processed_data = preprocess(data)

    prediction = lr_model.predict(processed_data)[0]

    result = (
        "Has Heart Disease"
        if prediction == 1
        else "No Heart Disease"
    )

    return jsonify({
        'model': 'Logistic Regression',
        'prediction': result
    })



@app.route('/api/predict/svm', methods=['POST'])

def predict_svm():

    data = request.json

    processed_data = preprocess(data)

    prediction = svm_model.predict(processed_data)[0]

    result = (
        "Has Heart Disease"
        if prediction == 1
        else "No Heart Disease"
    )

    return jsonify({
        'model': 'SVM',
        'prediction': result
    })



@app.route('/api/chat', methods=['POST'])

def chatbot():

    try:

        data = request.get_json()

        user_message = data['message']

        prompt = f"""

        You are an AI Heart Health Assistant.

        Your job is to answer ONLY questions related to:

        - Heart health
        - Cardiovascular diseases
        - Blood pressure
        - Cholesterol
        - ECG
        - Diabetes
        - Exercise
        - Healthy lifestyle
        - Mental wellbeing
        - Nutrition
        - General healthcare awareness

        Rules:

        1. Keep answers simple and beginner friendly.
        2. Be scientifically accurate.
        3. Give short and helpful responses.
        4. Do not provide dangerous medical advice.
        5. Always recommend consulting doctors
           for serious symptoms.
        6. Do not answer unrelated questions.

        User Question:
        {user_message}

        """

        response = chat_model.generate_content(prompt)

        return jsonify({
            'reply': response.text
        })

    except Exception as e:

        return jsonify({
            'reply': f'Error: {str(e)}'
        })



@app.errorhandler(404)

def not_found(error):

    return render_template('404.html'), 404



if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )