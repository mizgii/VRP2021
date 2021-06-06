from flask import Flask,render_template
from forms import SimForm
app = Flask(__name__)

@app.route('/')
@app.route('/about')
def about_page():
    return render_template('index.html')

@app.route('/simulation',methods=['GET', 'POST'])
def simulation_page():
	form = SimForm()
	return render_template('simulation.html',form=form)

