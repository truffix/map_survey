import folium
import pandas as pd
from flask import Flask, render_template
from folium.plugins import FloatImage
from datetime import datetime
import threading

app = Flask(__name__)

@app.route("/", methods=["GET"])
def status():
    print("/")
    return "Status: OK"

@app.route("/map", methods=["GET"])
def map():
    print("/map")
    return render_template("mymap.html")
    # return(my_map.get_root().render())

def generate_map():
    threading.Timer(5.0, generate_map).start()
    sheet_id = "1Ow1MSQzj_oCH-pPdS1J7AUqgFdz_nA9TZJg_9SGfpbw"
    sheet_name = "sheet9"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)
    df = df[df['X'].notna()]
    df = df[
        ['X', 'Y', 'Кадастровый номер', 'Вид работ', 'Дата постановки задачи', 'Дата выезда', 'Время выезда', 'Номер заявки (договора)',
         'Выезд выполнен?', 'Цвет', 'Иконка']]

    df.to_csv('data_survey.csv')
    m = folium.Map(location=[59.867566, 39.936021], zoom_start=7)
    image_file = 'https://geo35.ru/upload/CAllcorp2/995/9957d6a37c0ccdd4085cf7a739e7ca14.png'
    FloatImage(image_file, bottom=5, left=45).add_to(m)

    df = df.dropna(subset=['Y'])
    df = df.fillna('-')

    for index, row in df.iterrows():
        folium.Marker([row['X'], row['Y']],
                      popup=folium.Popup("<b>Договор</b> " + row['Номер заявки (договора)'] + "<br><b>Вид работ</b> " + row[
                          'Вид работ'] + "<br><b>Дата выезда</b> " + row[
                                             'Дата выезда'] + "<br><b>Время выезда</b> " +  row[
                                             'Время выезда'] + "<br><b>Кадастровый номер</b> " + row[
                                             'Кадастровый номер'], max_width=300),
                      icon=folium.Icon(color=row['Цвет'], icon=row['Иконка'], prefix='fa')).add_to(m)

    # Пример: exact_02042019_130203.csv
    #file_name = 'Выезды за все время\Выезды за все время_{}..html'.format(datetime.now().strftime("%d%m%Y_%H%M%S"))

    m.save("templates/mymap.html")


if __name__=="__main__":
    generate_map()
    print("Map is generated")

    app.run(host="0.0.0.0", port=4000, debug=True)