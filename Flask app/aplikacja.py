from flask import Flask,render_template, redirect, url_for
from forms import SimForm
from pndmodel import DataModel,Optimization


app = Flask(__name__)
app.config['SECRET_KEY'] = '9b807628f884d757930e1b4b'



@app.route('/')
@app.route('/about')
def about_page():
    return render_template('index.html')

@app.route('/simulation',methods=['GET', 'POST'])
def simulation_page():
    form = SimForm()
    if form.validate_on_submit():
        model = DataModel(n=form.points.data,
                              nv=form.number_vehicles.data,
                              cap=form.capacity.data)
        model=model.createmodel
        solution=Optimization(model,tlimit=form.tlimit.data)
        solstring=solution.textsol
        with open("templates/output.html","w") as file:
            file.write(solstring)

        return redirect(url_for('solution_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            print(f'There was an error with submitting: {err_msg}')

    return render_template('simulation.html', form=form)

@app.route('/solution')
def solution_page():
    return render_template('solution.html')

@app.route('/output.html')
def output_page():
    return render_template('output.html')
