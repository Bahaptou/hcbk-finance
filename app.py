from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import numpy as np
from bapt_functions import Ratios, Export, Sector


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
    if my_json_from_js['ticker'] not in my_companies_list :
        my_companies_list.append(my_json_from_js['ticker'])
    selected_frequency = my_json_from_js['selected_frequency']
    selected_ratio = my_json_from_js['selected_ratios']

    df = Sector.get_ratio_frame_frequency_company(companies_list=my_companies_list, frequency = selected_frequency, list_ratio=selected_ratio, sort_type = sort_by)

    date_list = []
    data_by_col_list = []
    if my_companies_list != []:
        

        for i in selected_ratio :
            data_one_ratio = []
            for j in list(df.columns.values):
                my_data_list = df.loc[[i],[j]].values.reshape(1,len(df.loc[[i],[j]]))[0].tolist()
                data_one_ratio.append(my_data_list)
            data_by_col_list.append(data_one_ratio)

        if sort_by == 'by_date':
            date_list = [list(df.index)[0][0]]
            cpt = 0
            for i in list(df.index) :
                if i[0] not in date_list:
                    date_list.append(i[0])
                    cpt+=1

            date_list.reverse()

        if sort_by == 'by_ratio':
            date_list = [list(df.index)[0][1]]
            cpt = 0
            for i in list(df.index) :
                if i[1] not in date_list:
                    date_list.append(i[1])
                    cpt+=1


    df = df.reset_index()



    return jsonify('', render_template('ratio_picture_data.html',ratios_list = list(Ratios.Ratios_switch.keys()),
                            col = selected_ratio, labels_list = date_list, column_names=list(df.columns.values),
                            col_data = data_by_col_list, row_data=list(df.values.tolist()), Zip=zip, link_column="Mean",
                            list_categorie_number = categorie_number_list, list_categorie_name = categorie_name_list,
                            possible_frequences_list = ['annual', 'quarterly'], all_companies_list = all_companies_list, 
                            companies_list = sorted(my_companies_list)))



@app.route('/del_comp', methods = ["POST"])

def del_comp():
    output = request.get_json()
    my_json_from_js = json.loads(output) #this converts the json output to a python dictionary
    my_companies_list.remove(my_json_from_js['ticker'])
    selected_frequency = my_json_from_js['selected_frequency']
    selected_ratio = my_json_from_js['selected_ratios']

    df = Sector.get_ratio_frame_frequency_company(companies_list=my_companies_list, frequency = selected_frequency, list_ratio=selected_ratio, sort_type = sort_by)

    date_list = []
    data_by_col_list = []
    if my_companies_list != []:
        

        for i in selected_ratio :
            data_one_ratio = []
            for j in list(df.columns.values):
                my_data_list = df.loc[[i],[j]].values.reshape(1,len(df.loc[[i],[j]]))[0].tolist()
                data_one_ratio.append(my_data_list)
            data_by_col_list.append(data_one_ratio)

        if sort_by == 'by_date':
            date_list = [list(df.index)[0][0]]
            cpt = 0
            for i in list(df.index) :
                if i[0] not in date_list:
                    date_list.append(i[0])
                    cpt+=1

            date_list.reverse()

        if sort_by == 'by_ratio':
            date_list = [list(df.index)[0][1]]
            cpt = 0
            for i in list(df.index) :
                if i[1] not in date_list:
                    date_list.append(i[1])
                    cpt+=1


    df = df.reset_index()



    return jsonify('', render_template('ratio_picture_data.html',ratios_list = list(Ratios.Ratios_switch.keys()),
                            col = selected_ratio, labels_list = date_list, column_names=list(df.columns.values),
                            col_data = data_by_col_list, row_data=list(df.values.tolist()), Zip=zip, link_column="Mean",
                            list_categorie_number = categorie_number_list, list_categorie_name = categorie_name_list,
                            possible_frequences_list = ['annual', 'quarterly'], all_companies_list = all_companies_list, 
                            companies_list = sorted(my_companies_list)))


@app.route('/reinit_comp', methods = ["POST"])

def reinit_comp():
    output = request.get_json()
    my_json_from_js = json.loads(output) #this converts the json output to a python dictionary
    my_companies_list.clear()
    selected_frequency = my_json_from_js['selected_frequency']
    selected_ratio = my_json_from_js['selected_ratios']

    df = Sector.get_ratio_frame_frequency_company(companies_list=my_companies_list, frequency = selected_frequency, list_ratio=selected_ratio, sort_type = sort_by)

    date_list = []
    data_by_col_list = []
    if my_companies_list != []:
        

        for i in selected_ratio :
            data_one_ratio = []
            for j in list(df.columns.values):
                my_data_list = df.loc[[i],[j]].values.reshape(1,len(df.loc[[i],[j]]))[0].tolist()
                data_one_ratio.append(my_data_list)
            data_by_col_list.append(data_one_ratio)

        if sort_by == 'by_date':
            date_list = [list(df.index)[0][0]]
            cpt = 0
            for i in list(df.index) :
                if i[0] not in date_list:
                    date_list.append(i[0])
                    cpt+=1

            date_list.reverse()

        if sort_by == 'by_ratio':
            date_list = [list(df.index)[0][1]]
            cpt = 0
            for i in list(df.index) :
                if i[1] not in date_list:
                    date_list.append(i[1])
                    cpt+=1


    df = df.reset_index()



    return jsonify('', render_template('ratio_picture_data.html',ratios_list = list(Ratios.Ratios_switch.keys()),
                            col = selected_ratio, labels_list = date_list, column_names=list(df.columns.values),
                            col_data = data_by_col_list, row_data=list(df.values.tolist()), Zip=zip, link_column="Mean",
                            list_categorie_number = categorie_number_list, list_categorie_name = categorie_name_list,
                            possible_frequences_list = ['annual', 'quarterly'], all_companies_list = all_companies_list, 
                            companies_list = sorted(my_companies_list)))

@app.route('/maj_list', methods = ["POST"])

def maj_list():
    output = request.get_json()
    my_json_from_js = json.loads(output) #this converts the json output to a python dictionary
    companies_categorie = list(Export.import_my_json("C:/Users/bapti/Documents/Finance/Algorithmes/API_Connection/export/"+my_json_from_js["categorie_name"]).keys())
    selected_frequency = my_json_from_js["selected_frequency"]
    selected_ratio = my_json_from_js["selected_ratios"]
    for i in companies_categorie : 
        if i not in my_companies_list :
            my_companies_list.append(i)

    df = Sector.get_ratio_frame_frequency_company(companies_list=my_companies_list, frequency = selected_frequency, list_ratio=selected_ratio, sort_type = sort_by)
    
    date_list = []
    data_by_col_list = []
    if my_companies_list != []:
        

        for i in selected_ratio :
            data_one_ratio = []
            for j in list(df.columns.values):
                my_data_list = df.loc[[i],[j]].values.reshape(1,len(df.loc[[i],[j]]))[0].tolist()
                data_one_ratio.append(my_data_list)
            data_by_col_list.append(data_one_ratio)

        if sort_by == 'by_date':
            date_list = [list(df.index)[0][0]]
            cpt = 0
            for i in list(df.index) :
                if i[0] not in date_list:
                    date_list.append(i[0])
                    cpt+=1

            date_list.reverse()

        if sort_by == 'by_ratio':
            date_list = [list(df.index)[0][1]]
            cpt = 0
            for i in list(df.index) :
                if i[1] not in date_list:
                    date_list.append(i[1])
                    cpt+=1


    df = df.reset_index()


    
    return jsonify('', render_template('ratio_picture_data.html', ratios_list = list(Ratios.Ratios_switch.keys()),
                            col = selected_ratio, labels_list = date_list, column_names=list(df.columns.values),
                            col_data = data_by_col_list, row_data=list(df.values.tolist()), Zip=zip, link_column="Mean",
                            list_categorie_number = categorie_number_list, list_categorie_name = categorie_name_list,
                            possible_frequences_list = ['annual', 'quarterly'], all_companies_list = all_companies_list, 
                            companies_list = sorted(my_companies_list)))


@app.route('/maj_data', methods=['POST'])
def maj_data():
    output = request.get_json()
    my_json_from_js = json.loads(output) #this converts the json output to a python dictionary
    selected_ratio = my_json_from_js["selected_ratios"]
    sector_number = my_json_from_js["categorie_name"][:2]
    selected_frequency = my_json_from_js["selected_frequency"]
    selected_companies= my_json_from_js["companies"]
    #df = Sector.get_ratio_frame_frequency(sector_number,frequency = selected_frequency, list_ratio=selected_ratio, sort_type = sort_by)
    df = Sector.get_ratio_frame_frequency_company(companies_list=selected_companies, frequency = selected_frequency, list_ratio=selected_ratio, sort_type = sort_by)
    date_list = []
    data_by_col_list = []
    if selected_companies != []:
        

        for i in selected_ratio :
            data_one_ratio = []
            for j in list(df.columns.values):
                my_data_list = df.loc[[i],[j]].values.reshape(1,len(df.loc[[i],[j]]))[0].tolist()
                data_one_ratio.append(my_data_list)
            data_by_col_list.append(data_one_ratio)

        if sort_by == 'by_date':
            date_list = [list(df.index)[0][0]]
            cpt = 0
            for i in list(df.index) :
                if i[0] not in date_list:
                    date_list.append(i[0])
                    cpt+=1

            date_list.reverse()

        if sort_by == 'by_ratio':
            date_list = [list(df.index)[0][1]]
            cpt = 0
            for i in list(df.index) :
                if i[1] not in date_list:
                    date_list.append(i[1])
                    cpt+=1


    df = df.reset_index()


    return jsonify('', render_template('ratio_picture_data.html', ratios_list = list(Ratios.Ratios_switch.keys()),
                            col = selected_ratio, labels_list = date_list, column_names=list(df.columns.values),
                            col_data = data_by_col_list, row_data=list(df.values.tolist()), Zip=zip, link_column="Mean",
                            list_categorie_number = categorie_number_list, list_categorie_name = categorie_name_list,
                            possible_frequences_list = ['annual', 'quarterly'], all_companies_list = all_companies_list, 
                            companies_list = sorted(my_companies_list)
                             ))




@app.route('/')
def homepage():

    df = Sector.get_ratio_frame_frequency(default_sector_number,frequency = the_frequence, list_ratio=selected_ratio, sort_type = sort_by)
    df = Sector.get_ratio_frame_frequency_company(companies_list=['AAPL'],frequency = the_frequence, list_ratio=selected_ratio, sort_type = sort_by)
    
    data_by_col_list = []

    for i in selected_ratio :
        data_one_ratio = []
        for j in list(df.columns.values):
            my_data_list = df.loc[[i],[j]].values.reshape(1,len(df.loc[[i],[j]]))[0].tolist()
            data_one_ratio.append(my_data_list)
        data_by_col_list.append(data_one_ratio)

    if sort_by == 'by_date':
        date_list = [list(df.index)[0][0]]
        cpt = 0
        for i in list(df.index) :
            if i[0] not in date_list:
                date_list.append(i[0])
                cpt+=1

        date_list.reverse()

    if sort_by == 'by_ratio':
        date_list = [list(df.index)[0][1]]
        cpt = 0
        for i in list(df.index) :
            if i[1] not in date_list:
                date_list.append(i[1])
                cpt+=1

        


    df = df.reset_index()

    return render_template('index.html', ratios_list = list(Ratios.Ratios_switch.keys()),
                            col = selected_ratio, labels_list = date_list, column_names=list(df.columns.values),
                            col_data = data_by_col_list, row_data=list(df.values.tolist()), Zip=zip, link_column="Mean",
                            list_categorie_number = categorie_list, list_categorie_name = categorie_name_list,
                            possible_frequences_list = ['annual', 'quarterly'], all_companies_list = all_companies_list,
                            companies_list = sorted(my_companies_list)
                            )


if __name__ == "__main__":
    app.run(debug=False)