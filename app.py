from flask import Flask, render_template, url_for
from datetime import datetime as dt
from jinja2 import Template

app = Flask(__name__)


def build_report():

    # opening files
    with open('conditions/abbreviations.txt', 'r') as f:
        f_contents = f.readlines()
        f_list = [line.split('_') for line in f_contents]

    with open('conditions/start.log', 'r') as log1:
        log1_contents = log1.readlines()
        log1_list = [line.split('_') for line in log1_contents]

    with open('conditions/end.log', 'r') as log2:
        log2_contents = log2.readlines()
        log2_list = [line.split('_') for line in log2_contents]

    # creating a list for every racer
    racers_report = [[racer, log1_item, log2_item] for racer in f_list for log1_item in log1_list for log2_item
                     in log2_list if racer[0] in log1_item[0] and racer[0] in log2_item[0]]

    # creating statistic string for one racer
    def statistic_string(stat_array):

        # calculating result of race
        time_start = dt.strptime(stat_array[1][1].rstrip(), '%H:%M:%S.%f')
        time_end = dt.strptime(stat_array[2][1].rstrip(), '%H:%M:%S.%f')
        time_race = str(abs(time_start - time_end))
        time_delta = dt.strptime(time_race, '%H:%M:%S.%f')
        result_of_race = time_delta.strftime('%M:%S.%f')[:-3]

        # creating statistic list
        stat_list = [[stat_array[0][1]], ['     | '], [stat_array[0][2].rstrip()], ['     | '], [result_of_race]]
        return stat_list

    # creating statistics list of strings for every racer
    all_racer_stat = list(map(statistic_string, racers_report))

    return all_racer_stat


def asc_report(all_racers_stat):

    # key for sorter list of racer
    def time_return(time_of_race):
        return time_of_race[4]

    # creating sorted racer list
    def asc_sorting_list():
        sorted_racers = sorted(all_racers_stat, key=time_return)
        racers_strings = ["".join(["".join(i) for i in racer]) for racer in sorted_racers]
        asc_sort = [f'{str(racers_strings.index(racer) + 1)} {racer}' for racer in racers_strings]
        return asc_sort

    final_asc_list = asc_sorting_list()

    return final_asc_list


asc_racers = asc_report(build_report())


def desc_report(all_racers_stat):

    # key for sorter list of racer
    def time_return(time_of_race):
        return time_of_race[4]

    # creating sorted racer list
    def desc_sorting_list():
        sorted_racers = sorted(all_racers_stat, key=time_return, reverse=True)
        racers_strings = ["".join(["".join(i) for i in racer]) for racer in sorted_racers]
        asc_sort = [f'{str(racers_strings[::-1].index(racer) + 1)} {racer}' for racer in racers_strings]
        return asc_sort

    final_desc_list = desc_sorting_list()

    return final_desc_list


desc_racers = desc_report(build_report())


def creating_list_of_drivers():
    with open('conditions/abbreviations.txt', 'r') as f:
        f_contents = f.readlines()
        f_list = [line.split('_') for line in f_contents]
        racers_list = []
        for i in range(len(f_list)):
            racers_list.append([f_list[i][0], f_list[i][1]])
        # list_of_drivers = [" ".join(driver) for driver in racers_list]
    return racers_list


drivers_list = creating_list_of_drivers()


@app.route('/')
def home_page():
    return render_template("home.html")


@app.route('/asc')
def asc_sorting():
    return render_template("asc_sorting.html", asc_racers=asc_racers)


@app.route('/desc')
def desc_sorting():
    return render_template("desc_sorting.html", desc_racers=desc_racers)


@app.route('/drivers')
def show_drivers_list():
    return render_template("driver_list.html", drivers_list=drivers_list)


@app.route('/drivers/<string:abbr>')
def driver_info(abbr):
    for racer in asc_racers:
        if abbr in racer:
            return render_template("driver_info.html", racer=racer)


if __name__ == '__main__':
    app.run(debug=True)

