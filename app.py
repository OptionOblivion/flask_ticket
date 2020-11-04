from flask import Flask, render_template,session,redirect,url_for
from flask_wtf import FlaskForm
from pymongo import collection
from wtforms import *
from wtforms.validators import DataRequired
from pymongo import MongoClient

#main Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '*********************'

#Database Link. DB Cluster redacted.
cluster= MongoClient('mongodb+srv://********************************')
db = cluster["*************"]
ticket_DB = db["tickets"]


#Submission Form Template
class SubmissionForm(FlaskForm):

    name = StringField('Enter you name: ', validators=[DataRequired()])
    email = StringField('Enter your email:', validators=[DataRequired()])
    type = RadioField('Please choose the catagory: ',
                         choices=[('Hardware','Hardware'),('Software','Software'), ('Other','Other')])
    department = SelectField(u'Choose your department:',
                                choices=[('Acct','Accounting'),('CS','Customer Service'),('Sales','Sales')])
    description = TextAreaField('Describe the issue:')
    submit = SubmitField('Submit Ticket')

    def ticketPost(self):
        ticket = {'name': self.name.data, 'email': self.email.data, 'department': self.department.data, 'description':self.description.data}
        ticket_DB.insert_one(ticket)
#HTML Pages
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SubmissionForm()
    if form.validate_on_submit():
        session['name']= form.name.data
        session['email']= form.email.data 
        session['type']= form.type.data
        session['department'] = form.department.data
        session['description']= form.description.data
        form.ticketPost()
        return redirect(url_for('ticket_submitted'))
        
    return render_template('index.html', form=form)

@app.route('/ticket_submitted')
def ticket_submitted():
    return render_template('ticket_submission.html')

if __name__ == '__main__':
    app.run()
