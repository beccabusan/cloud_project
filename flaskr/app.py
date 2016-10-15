from __future__ import absolute_import
from os import path, environ
import json
from flask import Flask, Blueprint, render_template, abort, jsonify, request, session, redirect, url_for
import settings
from celery import Celery
import sys


app = Flask(__name__)
app.config.from_object(settings)

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task(name="tasks.add")
def add(x, y):
    return x + y

@app.route("/calcajax")
def calc():
    def generate():
        x = 0
        while x < 100:
            print x
            x = x + 10
            time.sleep(0.4)
            yield "data:" + str(x) + "\n\n"
    return Response(generate(), mimetype="text/event-stream")

@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/calculating", methods=['post'])
def calculating():
    if request.method == 'POST':
        start_angle = request.form['start_angle']
        stop_angle = request.form['stop_angle']
    return render_template('calc.html', start_angle=start_angle, stop_angle=stop_angle)

@app.route("/test/result/<task_id>")
def show_result(task_id):
    retval = add.AsyncResult(task_id).get()
    return repr(retval)

if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
