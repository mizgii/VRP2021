from flask import Flask,render_template, redirect, url_for,send_file
from forms import SimForm
from pndmodel import DataModel,Optimization

#Application visualizing results of Pickup and Delivery optimization experiments
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
        model.drawpnd
        dmodel=model.createmodel
        solution=Optimization(dmodel,tlimit=form.tlimit.data,x=model.x,y=model.y)
        solstring=solution.textsol
        with open("templates/output.html","w") as file:
            file.write('<!doctype html><html lang="en"><head><!-- Required meta tags --><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous"></head><body>'+solstring+'</body><style>body { background-color: white; color: black}</style></html>')

        solution.drawsol
        return redirect(url_for('solution_page'))
    if form.errors != {}: #If there are errors from the validations
        for err_msg in form.errors.values():
            print(f'There was an error with submitting: {err_msg}')

    return render_template('simulation.html', form=form)

@app.route('/solution')
def solution_page():
    return render_template('solution.html')

@app.route('/output.html')
def output_page():
    return render_template('output.html')

@app.route('/figsol')
def figure_page():
    return send_file('figsol.png')

@app.route('/figpnd')
def pnd_page():
    return send_file('figpnd.png')

