from flask import jsonify, render_template
from  yahoofinancials import YahooFinancials as yf
import json
import pandas as pd
import unidecode as unic
import os
import numpy as np
import matplotlib.pyplot as plt

import_path = 'export'

class Export :

    def get_existant_categorie(myPath : str =  import_path) -> list[str]  :
        my_number_list =[]
        my_list_files = os.listdir(myPath)
        for i in my_list_files :
            my_number = i[:2]
            my_number = my_number.replace('_','')
            my_number_list.append(my_number)
        return sorted(my_number_list), sorted(my_list_files)


    def export_my_json (monjson : dict,myPath : str) -> None :
        tf = open(myPath, "w")
        json.dump(monjson,tf)
        tf.close()
        return None


    def import_my_json(myPath : str = import_path) -> dict:
        tf = open(myPath, "r")
        my_dict = json.load(tf)
        tf.close()
        return my_dict


    def format_name(original_name: str, number: int) -> str:
        myname = str(number)+'_'+unic.unidecode(original_name.split(' / ')[0].lower())
        for i in original_name.split(' / ')[1:]:
            myname+='_'+unic.unidecode(i.lower())
        myname+='_data.json'
        myname = myname.replace('(','')
        myname = myname.replace(')','')
        myname = myname.replace(' ','_')
        return myname


    def get_brut_data_one(ticker : str, type : list, frequency : list) -> dict :
        """
            The basic function that call YahooFinancials and sort the file

            Parameters
            --------

            ticker : str
                The ticker of the company
            
            type : str
                The type of statement you want
                Can be {'income', 'cash', 'balance'}
            
            frequency : str
                The last four quarter or the last four years
                Can be {'annual', 'quarterly'}

            Returns
            -------
            dict
                A dictionnary with the statement asked
        
        """
        
        statements = yf(ticker).get_financial_stmts(frequency, type)
        brut_file = {}
        for j in statements[list(statements.keys())[0]][ticker]:
            
            brut_file[list(j.keys())[0]] = j[list(j.keys())[0]]

        return brut_file


    def get_brut_stmt(ticker_list : list, type_list : list, frequency_list : list) -> dict:

        '''
            Fonction rendant un dictionnaire du type des financial statements demandés aux fréquences demandées pour les entreprises demandées

            Parameters : 
                ticker_list : list
                    Liste des tickers des entreprises
                type : list
                    Liste pouvant être constituée de 'cash', 'income', 'balance'.
                frequency : str
                    Liste pouvant être constituée de 'annual', 'quarterly'
        '''

        company_data ={}
        for i in ticker_list :
            stmt_data = {}
            for j in type_list :
                frequence_data = {}
                for k in frequency_list :
                    frequence_data[k] = Export.get_brut_data_one(i,j,k)
                stmt_data[j] = frequence_data
            company_data[i] = stmt_data
        

        return company_data


    def import_from_yahoo_stmt_json(self, ticker_categorie_frame : pd.DataFrame, categorie_number_list : list, myPath : str = import_path) -> None:

        for i in categorie_number_list :

            ticker_categorie_serie = ticker_categorie_frame.loc[ticker_categorie_frame[i].isna()==False,i]
            extract_data = self.get_brut_stmt(ticker_categorie_serie.iloc[1:],['balance','income','cash'],['annual','quarterly'])
            self.export_my_json(extract_data,myPath+'/'+self.format_name(ticker_categorie_serie.iloc[0],i))

        return None

    def get_json_from_categorie_number(categorie_number : str, myPath : str = import_path) -> dict :
            """Get the json file of the categorie number

            Parameters
            -------

            categorie_number : str
                The number of the sector wished

            myPath : str default import_path
                The Path where your files are

            Returns
            -------

            dict    
                The json you asked\n
                If wrong number, returns the dict :{'No such categorie number' : 'No such categorie number'}
            
            """
            my_list_files = os.listdir(myPath)
            try :
                my_name = list(filter(lambda x: categorie_number+'_' in x, my_list_files))[0]
            except IndexError as e:
                my_name = 'Error'

            if my_name[:len(categorie_number)+1] == categorie_number+'_' :
                return Export.import_my_json(myPath + '/' + my_name)
            else : 
                return {'No such categorie number' : {'No such categorie number': {'No such categorie number': {'No such categorie number' : {'No such categorie number' : 'No such categorie number'}}}}}




    def export_from_categories_to_companies(myPath : str = import_path) -> None:
        """Convert all categories json files into one json file of all companies

            The json file will be named 0_companies.json
            It will be exported on myPath

            Parameters
            -------

            myPath : str default import_path
                The path to your json files

            Returns
            -------

            None
                The json file of all companies in your Path

        """
        final_file = {}
        my_list_files = os.listdir(myPath)

        for i in my_list_files :

            my_json_file = Export.import_my_json(myPath+'/'+i)

            for j in my_json_file.keys():
                final_file = {**final_file, **my_json_file}

        
        Export.export_my_json(final_file,myPath+'/0_companies.json')

        return None



    def groupby_stmt_frame(my_dict : dict) -> dict:

        """Groupe in pd.DataFrame by statement.

        Parameters
        ----------

        my_dict : dict

            Dictionnary : companies-->type of statement-->frequency\n
            This dictionnary is basically the json imported by import_from_yahoo_stmt_json()

        Returns
        -------
        dict
            Dictionnary : type of statement-->frequency-->pd.DataFrame of the docs of all companies
        """

        doc_dict = {}
        final_list = []
        for i in my_dict[list(my_dict.keys())[0]]: #Donne les 3 types de documents

            freq_dict ={}

            for j in my_dict[list(my_dict.keys())[0]][i] : #Donne les 2 types de fréquences

                concat_list = []

                for k in list(my_dict.keys()) : #Donne le nom de l'entreprise

                    myframe = pd.DataFrame.from_dict(my_dict[k][i][j]) #Donne une frame du doc i à la fréquence j pour l'entreprise k

                    myframe.columns = pd.MultiIndex.from_tuples(zip([k, k, k, k],myframe.columns)) #Pour automatiser le remplissage des k, il faut une liste de k de la longeur de my_dict[k][j][i].keys()

                    concat_list.append(myframe)

                my_stmt = pd.concat(concat_list,axis=1)

                freq_dict[j] = my_stmt
            
            doc_dict[i] = freq_dict

        return doc_dict


    def export_my_excels(my_dict : dict, myPath : str = import_path+'/myfile.xlsx') -> None: #donnez aussi le nom de votre fichier en .xlsx
        """Export a json to an excel on your computer

        Parameters
        ----------

        my_dict : dict

            The json you want to export \n
            This dictionnary is basically the json imported by import_from_yahoo_stmt_json()

        my_Path : str

            The path to the place you want to export your file.\n
            Don't forget to right the name you want to give to your file

        Returns
        -------

        None  
        
        The file on your computer !
        """
        stmt_frame_grouped = Export.groupby_stmt_frame(my_dict)

        writer = pd.ExcelWriter(myPath)

        for i in stmt_frame_grouped : #le document

            for j in stmt_frame_grouped[i] : #la fréquence

                stmt_frame_grouped[i][j].to_excel(writer,str(i)+' '+str(j))
            

        writer.save()

        return None


    def reverse_columns_frame(the_frame : pd.DataFrame) -> pd.DataFrame:
        """Reverse the columns names of a pd.DataFrame

        Parameters
        -------

        the_frame : pd.DataFrame


        Returns
        -------

        pd.DataFrame

        The DataFrame with the columns reversed

        
        """

        return the_frame[the_frame.columns[::-1]]


class Ratios :


    def get_ROE_capital_stock(myjson : dict, ticker : str, date : int = 0, frequency : str = 'annual') -> float:
        return myjson[ticker]['cash'][frequency][list(myjson[ticker]['cash'][frequency])[date]]['netIncome']/(myjson[ticker]['balance'][frequency][list(myjson[ticker]['balance'][frequency])[date]]['capitalSurplus'] + myjson[ticker]['balance'][frequency][list(myjson[ticker]['balance'][frequency])[date]]['commonStock'])
    def get_ROE_equity(myjson : dict, ticker : str, date : int = 0, frequency : str = 'annual') -> float :
        return myjson[ticker]['cash'][frequency][list(myjson[ticker]['cash'][frequency])[date]]['netIncome']/myjson[ticker]['balance'][frequency][list(myjson[ticker]['balance'][frequency])[date]]['totalStockholderEquity']
    def get_net_profit_margin(myjson : dict, ticker : str, date : int = 0, frequency : str = 'annual') -> float :
        return myjson[ticker]['cash'][frequency][list(myjson[ticker]['cash'][frequency])[date]]['netIncome']/myjson[ticker]['income'][frequency][list(myjson[ticker]['income'][frequency])[date]]['totalRevenue']
    def get_ebitda_margin(myjson : dict, ticker : str, date : int = 0, frequency : str = 'annual') -> float :
        return (myjson[ticker]['income'][frequency][list(myjson[ticker]['income'][frequency])[date]]['ebit'] + myjson[ticker]['cash'][frequency][list(myjson[ticker]['cash'][frequency])[date]]['depreciation'])/myjson[ticker]['income'][frequency][list(myjson[ticker]['income'][frequency])[date]]['totalRevenue']
    def get_ebit_margin(myjson : dict, ticker : str, date : int = 0, frequency : str = 'annual') -> float :
        return myjson[ticker]['income'][frequency][list(myjson[ticker]['income'][frequency])[date]]['ebit']/myjson[ticker]['income'][frequency][list(myjson[ticker]['income'][frequency])[date]]['totalRevenue']
    def get_tax_burden_IBT(myjson : dict, ticker : str, date : int = 0, frequency : str = 'annual') -> float :
        return myjson[ticker]['cash'][frequency][list(myjson[ticker]['cash'][frequency])[date]]['netIncome']/myjson[ticker]['cash'][frequency][list(myjson[ticker]['cash'][frequency])[date]]['incomeBeforeTax']
    def get_tax_burden_TE(myjson : dict, ticker : str, date : int = 0, frequency : str = 'annual') -> float :
        return 1 + myjson[ticker]['cash'][frequency][list(myjson[ticker]['cash'][frequency])[date]]['netIncome']/myjson[ticker]['income'][frequency][list(myjson[ticker]['income'][frequency])[date]]['incomeTaxExpense']
    def default_function(myjson : dict, ticker : str, date : int = 0, frequency : str = 'annual') -> str:
        return 'Ration not found'

    Ratios_switch = {'ROE_Capital_Stock' : get_ROE_capital_stock, 'ROE_Equity' : get_ROE_equity, 'Net_Profit_Margin' :get_net_profit_margin, 'Ebitda_Margin' :get_ebitda_margin, 'Ebit_Margin' :get_ebit_margin, 'Tax_Burden_IBT' :get_tax_burden_IBT, 'Tax_Burden_TE':get_tax_burden_TE}
    
    class Ratios_Names: # Possible values
        """Ratios callable
        """
        
        ROE_Capital_Stock ='ROE_Capital_Stock'
        ROE_Equity = 'ROE_Equity'
        Net_Profit_Margin = 'Net_Profit_Margin'
        Ebitda_Margin = 'Ebitda_Margin'
        Ebit_Margin = 'Ebit_Margin'
        Tax_Burden_IBT = 'Tax_Burden_IBT'
        Tax_Burden_TE = 'Tax_Burden_TE'
        

class Sector :
      
    def get_ratio_frame(my_import_json : dict, list_ratio : list[str] = list(Ratios.Ratios_switch.keys()), date : int = 0, frequency : str = 'annual', myPath : str = import_path) -> pd.DataFrame :
        """Get a pd.DataFrame of the list of ratios.

            Parameters
            -------

            my_import_json : dict

            list_ratio : list[str] default all possible ratios
                The list that contains the ratios you want
                Can be : {'ROE Capital Stock','ROE Equity','Net Profit Margin','Ebitda Margin','Ebit Margin','Tax Burden IBT','Tax Burden TE'}

            date : int default 0
                Can be {0, 1, 2, 3}. 0 is the nearest, 3 the further.

            frequency : str default 'annual'
                Can be {'annual','quarterly'}

            myPath : str default import_path
                The Path where your files are

            
            Returns
            -------

            pd.DataFrame
                A DataFrame for wich columns are companies tickers and index are ratios names
        """

        my_frame = pd.DataFrame(columns=list(my_import_json.keys()))
        for i in list_ratio:
            my_list_data = []
            for j in my_import_json.keys() :
                try :
                    my_list_data.append(Ratios.Ratios_switch.get(i,Ratios.default_function)(my_import_json,j,date,frequency))
                except KeyError as e:
                    my_list_data.append(None)
                except TypeError as e :
                    my_list_data.append(None)
                except ZeroDivisionError as e :
                    my_list_data.append(None)
                except IndexError as e:
                    my_list_data.append(None)
            my_array = np.array(my_list_data)
            my_frame.loc[i] = my_array

        my_frame = pd.concat([my_frame,my_frame.mean(axis=1).to_frame(name = 'Mean'),my_frame.median(axis=1).to_frame(name = 'Median')],axis=1)
            

        return my_frame

    def get_ratio_frame_frequency(categorie_number : str, sort_type : str = 'by_date', list_ratio : list[str] = list(Ratios.Ratios_switch.keys()), frequency : str = 'annual', myPath : str = import_path) -> pd.DataFrame :
        """Get ratios of all the statements by date

        Parameters
        -------

            categorie_number : int
            The number of the sector wished

            sort_type : str default 'by_date'
                Can be {'by_date', 'by_ratio'}
                Sort the return DataFrame by date or by ratio

            list_ratio : list[str] default all possible ratios
                The list that contains the ratios you want
                Can be : {'ROE Capital Stock','ROE Equity','Net Profit Margin','Ebitda Margin','Ebit Margin','Tax Burden IBT','Tax Burden TE'}

            frequency : str default 'annual'
                Can be {'annual','quarterly'}

            myPath : str default import_path
                The Path where your files are

        Returns
        -------

        pd.DataFrame
            A DataFrame for wich columns are companies tickers and index are ratios names and date

        """

        my_import_json = Export.get_json_from_categorie_number(categorie_number, myPath)
        my_list_of_frame = []

        
        my_list_of_date = []


        for i in range(len(my_import_json[list(my_import_json.keys())[0]][list(my_import_json[list(my_import_json.keys())[0]].keys())[0]][list(my_import_json[list(my_import_json.keys())[0]][list(my_import_json[list(my_import_json.keys())[0]].keys())[0]].keys())[0]].keys())) :

            my_list_of_frame.append(Sector.get_ratio_frame(my_import_json,list_ratio,i,frequency))
            for j in range(len(my_list_of_frame[0])):
                my_list_of_date.append(list(my_import_json[list(my_import_json.keys())[0]][list(my_import_json[list(my_import_json.keys())[0]].keys())[0]][frequency])[i][:7])

        
        
        tot_frame = pd.concat(my_list_of_frame, axis=0)
        my_list_of_index = list(tot_frame.index)

        tuples = list(zip(*[my_list_of_date,my_list_of_index]))

        index = pd.MultiIndex.from_tuples(tuples, names=["Date", "Ratio"])

        tot_frame.index = index

        if sort_type == 'by_date' :
            return tot_frame
        elif sort_type == 'by_ratio' :
            return tot_frame.swaplevel().sort_index()

    def get_ratio_graph (categorie_number : int, grap_size : int = 5, list_ratio : list[str] = list(Ratios.Ratios_switch.keys()), frequency : str = 'annual', myPath : str = import_path) -> plt.show() :
            
        """Get grahs of all the statements by date

        Parameters
        -------

            categorie_number : int
            The number of the sector wished

            graph_size : int default 5
                Higher is the number, bigger is the graph

            list_ratio : list[str] default all possible ratios
                The list that contains the ratios you want
                Can be : {'ROE Capital Stock','ROE Equity','Net Profit Margin','Ebitda Margin','Ebit Margin','Tax Burden IBT','Tax Burden TE'}

            frequency : str default 'annual'
                Can be {'annual','quarterly'}

            myPath : str default import_path
                The Path where your files are

        Returns
        -------

        plt.show()
            Graphs

        """

        my_frame = Sector.get_ratio_frame_frequency(categorie_number, sort_type = 'by_ratio', list_ratio = list_ratio, frequency = frequency, myPath = myPath )
        cpt = 0
        fig = plt.figure(figsize=(10,len(list_ratio)*grap_size))
        for i in range(len(list_ratio)) :
            ax = fig.add_subplot(len(list_ratio),1,i+1)
            ax.plot(my_frame.loc[list_ratio[i]])
            ax.set_title(list_ratio[i])
            ax.legend(my_frame.columns, loc = 'upper left')

        return plt.show()

    
    def get_ratio_frame_company(my_import_json : dict, list_ratio : list[str] = list(Ratios.Ratios_switch.keys()), date : int = 0, frequency : str = 'annual', myPath : str = import_path) -> pd.DataFrame :
        """Get a pd.DataFrame of the list of ratios.

            Parameters
            -------

            my_import_json : dict

            list_ratio : list[str] default all possible ratios
                The list that contains the ratios you want
                Can be : {'ROE Capital Stock','ROE Equity','Net Profit Margin','Ebitda Margin','Ebit Margin','Tax Burden IBT','Tax Burden TE'}

            date : int default 0
                Can be {0, 1, 2, 3}. 0 is the nearest, 3 the further.

            frequency : str default 'annual'
                Can be {'annual','quarterly'}

            myPath : str default import_path
                The Path where your files are

            
            Returns
            -------

            pd.DataFrame
                A DataFrame for wich columns are companies tickers and index are ratios names
        """

        my_frame = pd.DataFrame(columns=list(my_import_json.keys()))
        for i in list_ratio:
            my_list_data = []
            for j in my_import_json.keys() :
                try :
                    my_list_data.append(Ratios.Ratios_switch.get(i,Ratios.default_function)(my_import_json,j,date,frequency))
                except KeyError as e:
                    my_list_data.append(None)
                except TypeError as e :
                    my_list_data.append(None)
                except ZeroDivisionError as e :
                    my_list_data.append(None)
                except IndexError as e:
                    my_list_data.append(None)
            my_array = np.array(my_list_data)
            my_frame.loc[i] = my_array

        my_frame = pd.concat([my_frame,my_frame.mean(axis=1).to_frame(name = 'Mean'),my_frame.median(axis=1).to_frame(name = 'Median')],axis=1)
            

        return my_frame

    def get_ratio_frame_frequency_company(companies_list : list[str], sort_type : str = 'by_date', list_ratio : list[str] = list(Ratios.Ratios_switch.keys()), frequency : str = 'annual', myPath : str = import_path) -> pd.DataFrame :
            """Get ratios of all the statements by date

            Parameters
            -------

                companies_list : list[str]
                The list of the tickers wished

                sort_type : str default 'by_date'
                    Can be {'by_date', 'by_ratio'}
                    Sort the return DataFrame by date or by ratio

                list_ratio : list[str] default all possible ratios
                    The list that contains the ratios you want
                    Can be : {'ROE Capital Stock','ROE Equity','Net Profit Margin','Ebitda Margin','Ebit Margin','Tax Burden IBT','Tax Burden TE'}

                frequency : str default 'annual'
                    Can be {'annual','quarterly'}

                myPath : str default import_path
                    The Path where your files are

            Returns
            -------

            pd.DataFrame
                A DataFrame for wich columns are companies tickers and index are ratios names and date

            """
            if companies_list != [] and list_ratio != []:
                my_import_json = Export.get_json_from_categorie_number("00", myPath)
                my_companies_json = {}


                for j in companies_list :
                    my_companies_json[j] = my_import_json[j]


                my_list_of_frame = []        
                my_list_of_date = []


                for i in range(len(my_companies_json[list(my_companies_json.keys())[0]][list(my_companies_json[list(my_companies_json.keys())[0]].keys())[0]][list(my_companies_json[list(my_companies_json.keys())[0]][list(my_companies_json[list(my_companies_json.keys())[0]].keys())[0]].keys())[0]].keys())) :

                    my_list_of_frame.append(Sector.get_ratio_frame_company(my_companies_json,list_ratio,i,frequency))
                    for j in range(len(my_list_of_frame[0])):
                        my_list_of_date.append(list(my_companies_json[list(my_companies_json.keys())[0]][list(my_companies_json[list(my_companies_json.keys())[0]].keys())[0]][frequency])[i][:7])

                
                
                tot_frame = pd.concat(my_list_of_frame, axis=0)
                my_list_of_index = list(tot_frame.index)

                tuples = list(zip(*[my_list_of_date,my_list_of_index]))

                index = pd.MultiIndex.from_tuples(tuples, names=["Date", "Ratio"])

                tot_frame.index = index

                if sort_type == 'by_date' :
                    return tot_frame
                elif sort_type == 'by_ratio' :
                    return tot_frame.swaplevel().sort_index()
                    
            elif  companies_list == [] and list_ratio != []:
                my_list_of_date = []
                my_list_of_index = []
                my_false_data = []
                for i in list_ratio:
                    for j in range(4):
                        my_list_of_index.append(i)
                        my_list_of_date.append('Date'+str(j))
                        my_false_data.append('None')

                tuples = list(zip(*[my_list_of_index,my_list_of_date]))
                index = pd.MultiIndex.from_tuples(tuples, names=["Ratio","Date"])
                    
                return pd.DataFrame(columns=['Entreprise'], data=my_false_data, index=index)
            
            elif companies_list != [] and list_ratio == []:
                my_false_data = []
                for i in range(len(companies_list)):
                    my_false_data.append('None')
                return pd.DataFrame(columns=companies_list, data=[my_false_data], index=[['Ratio'],['Date']])

            elif companies_list == [] and list_ratio == []:
                return pd.DataFrame(columns=['Entreprise'], data=['None'], index=[['Ratio'],['Date']])

class HCBK_web :

    def all_data_sorted(all_companies_list : list[str] ,my_template : str, companies_list : list[str], sort_type : str = 'by_date', list_ratio : list[str] = list(Ratios.Ratios_switch.keys()), frequency : str = 'annual', myPath : str = import_path) -> dict :


        df = Sector.get_ratio_frame_frequency_company(companies_list, sort_type, list_ratio, frequency, myPath)
        df = df.transpose()
        date_list = []
        data_by_col_list = []
        try :
            col = df.columns.levels[0].values.tolist()
        except AttributeError as e :
            col = list_ratio
        if companies_list != []:

            for i in col :
                data_by_col_list.append(df[i].values.tolist())

            if sort_type == 'by_date':
                date_list = [df.columns.to_list()[0][0]]
                cpt = 0
                for i in df.columns.to_list() :
                    if i[0] not in date_list:
                        date_list.append(i[0])
                        cpt+=1

                date_list.reverse()

            if sort_type == 'by_ratio':
                date_list = [df.columns.to_list()[0][1]]
                cpt = 0
                for i in df.columns.to_list() :
                    if i[1] not in date_list:
                        date_list.append(i[1])
                        cpt+=1

        columns_names = df.index.to_list()
        df = df.reset_index()

        #del
        #add
        #reinit
        #categorie
        #maj_ratio_frequency
        render = {}
        render['my_template'] = my_template
        render['ratios_list'] = list(Ratios.Ratios_switch.keys()) 
        render['col'] = col 
        render['labels_list'] = date_list
        render['column_names'] = columns_names 
        render['col_data'] = data_by_col_list 
        render['row_data'] = df.values.tolist() 
        render['Zip'] = zip 
        render['link_column'] = "Mean" 
        render['possible_frequences_list'] = ['annual', 'quarterly'] 
        render['all_companies_list'] = all_companies_list 
        render['companies_list'] = sorted(companies_list) 
       

        return render_template(render['my_template'], ratios_list = render['ratios_list'], col = render['col'],
            labels_list = render['labels_list'], column_names = render['column_names'], col_data = render['col_data'],
            row_data = render['row_data'], Zip = render['Zip'], link_column = render['link_column'],
            list_categorie_number = Export.get_existant_categorie()[0], list_categorie_name = Export.get_existant_categorie()[1], all_companies_list = all_companies_list,
            possible_frequences_list = render['possible_frequences_list'], companies_list = render['companies_list'])
    