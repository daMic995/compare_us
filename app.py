from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session)

import compare
# Create an instance of Flask
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("compare.html")

@app.route("/compare")
def compare():
    link_1 = request.args.get("link_1")
    link_2 = request.args.get("link_2")

    product_1 = compare.amzn_get_details_from_url(link_1)
    product_2 = compare.amzn_get_details_from_url(link_2)

    details_1 = compare.amzn_get_product_details(product_1)
    details_2 = compare.amzn_get_product_details(product_2)

    return(render_template("compare.html", item_1=details_1, item_2=details_2))