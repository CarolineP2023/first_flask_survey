from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "surveys"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = []
reponses = []

@app.route('/')
def home_page():
    """start survey"""

    return render_template('home.html', survey=survey)


@app.route('/', methods=['POST'])
def set_session():
    return redirect("home.html")


@app.route('/start', method = ["POST"])
def start_survey():
    """used to start the survey redirects to the first question"""

    session[RESPONSES_KEY] = []
    return redirect("/question/0")



@app.route('/question/<int:ques_id>')
def questions(ques_id):
    """"displays questions"""
    responses = session.get(RESPONSES_KEY)
    if(len(responses) == len(survey.questions)):
        # if its the end of the survey display thank you
        return redirect("/thanks")
    if(len(responses) != ques_id):
        #if user is trying to access a question not in the survey
        flash(f"Invalid question request")
        return redirect(f"/question/{len(responses)}")
    if(responses is None):
        #if user tries to move on without answering
        return redirect("/")

    question = survey.questions[ques_id]
    return render_template('questions.html',question_num=ques_id, question=question)


@app.route('/answer', methods=["POST"])
def get_answers():
    """gets users answer"""
    answer = request.form['answer']
    text = request.form.get("text", "")

    responses = session[RESPONSES_KEY]
    responses.append({"answer": answer, "text": text})

    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        #if the users has answered the last question takes them to the complete page
        return redirect("/thanks")
    else:
        return redirect(f"/question/{len(responses)}")


@app.route('/thanks')
def survey_complete():
    """displays survey complete page"""
    responses = session[RESPONSES_KEY]
    return render_template("complete.html")
