from flask import Flask,render_template
from forms import SimForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '40dc9ffb03a681a2243d7347'


@app.route('/')
@app.route('/about')
def about_page():
    return render_template('index.html')

@app.route('/simulation',methods=['GET', 'POST'])
def simulation_page():
	form = SimForm()
	return render_template('simulation.html',form=form)
