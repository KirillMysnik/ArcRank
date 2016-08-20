from flask import jsonify, render_template

from . import app, config


@app.route('/')
def route_index():
    return render_template("arcrank.html")


@app.route('/ajax-init', methods=['POST', ])
def route_ajax_init():
    return jsonify({
        'nav-links': config['navigation']['nav-links'],
        'languages': config['application']['languages'],
    })
