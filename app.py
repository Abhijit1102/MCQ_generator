from flask import Flask, render_template, request, jsonify
import json
import os 
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI

app = Flask(__name__)

TEMPLATE = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

TEMPLATE2 = """
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at par with the cognitive and analytical abilities of the students,\
update the quiz questions which need to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_file = 'quiz.json'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        api_key = request.form['apiKey']
        print(api_key)
        SUBJECT = request.form['subject']
        print(SUBJECT)
        TONE = request.form['ton']
        print(TONE)
        NUMBER = int(request.form['numQuestions'])
        print(NUMBER)
        file_upload = request.files['fileUpload']
        if file_upload:
            # Save the uploaded text file
            file_upload.save(f'uploads/{file_upload.filename}')
            file_path = f'uploads/{file_upload.filename}'
            print(f'File uploaded successfully. Path: {file_path}')

        with open(file_path, 'r') as file:
            TEXT = file.read()
           # print(TEXT)

        with open('Response.json') as json_file:
            RESPONSE_JSON = json.load(json_file)
           # print(RESPONSE_JSON)

        llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo", temperature=0.5)

        quiz_generation_prompt = PromptTemplate(
            input_variables=["text", "number", "subject", "tone", "response_json"],
            template=TEMPLATE
        )
        quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)
        quiz_evaluation_prompt = PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE)

        review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

        generate_evaluate_chain = SequentialChain(chains=[quiz_chain, review_chain],
                                                  input_variables=["text", "number", "subject", "tone", "response_json"],
                                                  output_variables=["quiz", "review"], verbose=True)

        with get_openai_callback() as cb:
            response = generate_evaluate_chain(
                {
                    "text": TEXT,
                    "number": NUMBER,
                    "subject": SUBJECT,
                    "tone": TONE,
                    "response_json": json.dumps(RESPONSE_JSON)
                }
            )


        #print(response)  
        quiz=response.get("quiz")  
        quiz=json.loads(quiz)
        #print(quiz)

        # Save the JSON data obtained from the response
        with open('quiz.json', 'w') as file:
            json.dump(quiz, file)

       # print('Quiz data saved to quiz.json')

    with open('quiz.json') as json_file:
        quiz_data = json.load(json_file)

    return render_template("quiz.html", quiz_data=quiz_data)

@app.route('/result', methods=['GET', 'POST'])
def result():
    user_responses = {}

    for question_number in request.form:
        user_response = request.form[question_number]
        question_number = question_number.replace('question', '')
        user_responses[question_number] = user_response

    # print("user_responses:", user_responses)

    with open('quiz.json') as json_file:
        quiz_data = json.load(json_file)

   # print("quiz_data:", quiz_data)

    return render_template("result.html", user_responses=user_responses, quiz_data=quiz_data)

    

if __name__ == '__main__':
    app.run(debug=True)
