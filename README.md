# Quiz Generator and Evaluator Web App

This web application allows users to generate and evaluate multiple-choice quizzes using the OpenAI GPT-3.5-turbo model. The application is built using Flask, a Python web framework.

## Features

- **Quiz Generation:** Users can input a text, specify the subject, tone, and the number of multiple-choice questions they want to generate. The application then uses the OpenAI GPT-3.5-turbo model to create the quiz.

- **Quiz Evaluation:** The generated quiz can be evaluated by an expert English grammarian and writer. The application analyzes the complexity of the questions and provides feedback. If necessary, the questions and tone can be updated.

- **User Interaction:** The web app allows users to interact with the application through a simple user interface. Users can input the necessary details and upload a text file for quiz generation.

- **Result Analysis:** Users can view the results of their quizzes and see how their responses compare to the generated quiz.

## Project Structure

- **`app.py`:** This is the main Flask application file that contains the routes and logic for the web app.

- **`templates/`:** This directory contains HTML templates for rendering different pages of the web app.

- **`uploads/`:** This directory is used to store uploaded text files.

- **`quiz.json`:** The generated quiz is stored in this JSON file.

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/Abhijit1102/2.MCQ_generator.git


2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the Flask application:
   ```bash
   python app.py

## Usage
- 1. Access the home page at http://localhost:5000.

- 2. Fill in the required details on the quiz generation page.

- Upload a text file for quiz generation.

- Click the "Submit" button.

- View the generated quiz and expert evaluation on the result page


### Acknowledgments
- This project uses the OpenAI GPT-3.5-turbo model. Make sure to use a valid OpenAI API key for proper functioning.

   
   
