from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import numpy as np
from bapt_functions import Ratios, Export, Sector, HCBK_web


app = Flask(__name__)
my_decimal = np.random.rand()
selected_ratio = list(Ratios.Ratios_switch.keys())[:2]
categorie_list = Export.get_existant_categorie()
categorie_number_list = categorie_list[0]
default_sector_number = categorie_number_list[1]
categorie_name_list = categorie_list[1]
sort_by = 'by_ratio'
the_frequence = 'annual'
all_companies_list = list(Export.import_my_json("export/00_companies.json").keys())
my_companies_list = []

@app.route('/add_comp', methods = ["POST"])

def add_comp():
    output = request.get_json()
    my_json_from_js = json.loads(output) #this converts the json output to a python dictionary
    selected_frequency = my_json_from_js['selected_frequency']
    selected_ratio = my_json_from_js['selected_ratios']
    list_companies = my_json_from_js['companies']
    if my_json_from_js['ticker'] not in list_companies :
        list_companies.append(my_json_from_js['ticker'])

    return HCBK_web.all_data_sorted(all_companies_list = all_companies_list, my_template='ratio_picture_data.html',
        companies_list=list_companies, sort_type=sort_by, list_ratio=selected_ratio, frequency=selected_frequency)


@app.route('/del_comp', methods = ["POST"])

def del_comp():
    output = request.get_json()
    my_json_from_js = json.loads(output) #this converts the json output to a python dictionary
    selected_frequency = my_json_from_js['selected_frequency']
    selected_ratio = my_json_from_js['selected_ratios']
    list_companies = my_json_from_js['companies']
    list_companies.remove(my_json_from_js['ticker'])

    return HCBK_web.all_data_sorted(all_companies_list = all_companies_list, my_template='ratio_picture_data.html',
        companies_list= list_companies, sort_type=sort_by, list_ratio=selected_ratio, frequency=selected_frequency)




@app.route('/reinit_comp', methods = ["POST"])

def reinit_comp():
    output = request.get_json()
    my_json_from_js = json.loads(output) #this converts the json output to a python dictionary
    selected_frequency = my_json_from_js['selected_frequency']
    selected_ratio = my_json_from_js['selected_ratios']

    return HCBK_web.all_data_sorted(all_companies_list = all_companies_list, my_template='ratio_picture_data.html',
        companies_list= [], sort_type=sort_by, list_ratio=selected_ratio, frequency=selected_frequency)

@app.route('/maj_list', methods = ["POST"])

def maj_list():
    output = request.get_json()
    my_json_from_js = json.loads(output) #this converts the json output to a python dictionary
    companies_categorie = list(Export.import_my_json("export/"+my_json_from_js["categorie_name"]).keys())
    selected_frequency = my_json_from_js["selected_frequency"]
    selected_ratio = my_json_from_js["selected_ratios"]
    list_companies = my_json_from_js['companies']


    for i in companies_categorie : 
        if i not in list_companies :
            list_companies.append(i)

    return HCBK_web.all_data_sorted(all_companies_list = all_companies_list, my_template='ratio_picture_data.html',
            companies_list=list_companies, sort_type=sort_by, list_ratio=selected_ratio, frequency=selected_frequency)


@app.route('/maj_data', methods=['POST'])
def maj_data():
    output = request.get_json()
    my_json_from_js = json.loads(output) #this converts the json output to a python dictionary
    selected_ratio = my_json_from_js["selected_ratios"]
    selected_frequency = my_json_from_js["selected_frequency"]
    selected_companies= my_json_from_js["companies"]

    return HCBK_web.all_data_sorted(all_companies_list = all_companies_list, my_template='ratio_picture_data.html',
            companies_list=selected_companies, sort_type=sort_by, list_ratio=selected_ratio, frequency=selected_frequency)




@app.route('/')
def homepage():

    return HCBK_web.all_data_sorted(all_companies_list = all_companies_list, my_template='index.html', companies_list=[], sort_type=sort_by, list_ratio=selected_ratio, frequency=the_frequence)


if __name__ == "__main__":
    app.run(debug=True)