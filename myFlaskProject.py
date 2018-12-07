from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import abort
import os
import handledata
import re
import json
import copy



app = Flask(__name__)
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))


@app.route("/")
def website_index():
    '''A route to the website index page named "/" with Flask. The index website
     displays a maximum of five of the newest projects and the latest projects
     based on project id are collected from the database in a new list. The
     database is sorted in a reversed order, since the newest project will have
     the highest project id. The information gathered are the modified database
     as well as the information about the author of the portfolio. This returns
     a Jinja2 rendered template with the gathered information with a Flask built
      in function.'''
    db = get_data()
    author = get_author_data()

    # Check to see if the database with projects is longer than five projects.
    # The index website displays the five newest projects sorted by project ID.
    if len(db)> 5:
        db = db[-5:]
    db.reverse()

    db = set_default_values(db)

    return render_template("index.html", author=author, db=db)


@app.route("/list")
def project_list():
    '''A Route for the project list page named "/list page" with Flask. Saves
    information about the current search possibilities, current search bar
    string and other search parameters selected by the user. This returns a
    Jinja2 rendered template with the gathered information with a Flask built in
     function.'''

    # Get all search possibilities for the project list.
    technique_list = get_all_techniques()
    search_field_list = get_all_search_fields()
    sortby_field_list = get_all_sortby_fields()

    # Get search string from the search bar
    search_string = get_request_args("search")["search"]

    # Get selected techniques, search fields, sort by field and sort by order.
    selected_techniques = get_selected_techniques_for_search()
    selected_search_fields = get_selected_fields_for_search()
    selected_search_fields = None if len(selected_search_fields) == 0 else selected_search_fields
    selected_sortby_field = get_selected_sortby_field_for_search()
    selected_search_order_field = get_selected_sortorder_field_for_search()


    db = get_data()

    db = handledata.search(db, sort_by=selected_sortby_field, sort_order=selected_search_order_field, techniques=selected_techniques, search=search_string, search_fields=selected_search_fields)

    db = set_default_values(db)


    return render_template("projectlist.html", db = db, technique_list = technique_list, search_fields=search_field_list, sortby_fields = sortby_field_list)


@app.route("/techniques")
def project_techniques():
    '''A Route for the technique page named "/techniques" with Flask.
    Information about the selected techniques on the website are gathered in a
    list, the information about the projects in the database that used the
    selected techniques are gathered in a list. There is also a list containing
    all the technique used in all projects, this is mainly used to display all
    the technique buttons on the website. This returns a Jinja2 rendered
    template with the gathered information with a Flask built in function.'''

    # Get the selected values from the technique page and split each search
    # value into a list.
    args = get_request_args('selected_techniques')
    selected_techniques = args['selected_techniques']
    selected_techniques_list = selected_techniques.split(',') if selected_techniques else []

    # Get the project from the database that used the selected techniques.
    project_list = get_projects_by_selected_techniques(selected_techniques_list)
    project_list = set_default_values(project_list)

    # Gather all used techniques from all the project in the database.
    technique_list = [{'label': technique, 'selected': technique in selected_techniques_list} for technique in get_all_techniques()]

    # Design on technique buttons.
    assign_random_wing_pair_to_technique_list(technique_list)

    # Generate form value for each button
    for technique in technique_list:
        if selected_techniques and technique['selected'] == True:
            technique['form_value'] = form_value_remove_item(selected_techniques, technique['label'])
        else:
            technique['form_value'] = form_value_add_item(selected_techniques, technique['label'])

    return render_template("techniques.html", technique_list = technique_list, project_list = project_list)



@app.route("/project/<int:id>")
def show_project(id = None):
    '''A route for a specific project page named "/project/<int:id>" with Flask.
     This collects all the data for a specific project and collects the name of
     the project images from the mapstructure.  This returns a Jinja2 rendered
     template with the gathered information with a Flask built in function.'''

    project = [get_project(id)]

    if not project[0]:
        abort(404)

    project_list = set_default_values(project)
    project = project_list[0]

    return render_template("projectpage.html", project=project)



# --- Data Help Functions ---

def get_data():
    '''Simplified method to load our json database file.'''
    json_url = os.path.join(PROJECT_ROOT, 'data.json')
    return handledata.load(json_url)


def get_project(id):
    '''Get a single project by it's id from the default json database.'''
    db = get_data()
    return handledata.get_project(db, id)


def get_all_techniques():
    '''Returns all techniques as a list of strings from the default json
    database.'''
    db = get_data()
    return handledata.get_techniques(db)

def get_all_search_fields():
    '''Returns all search fields that can be selected on the search page.'''
    search_fields = [("project_name", "Project name"),("start_date", "Start date"), ("end_date", "End date"), ("group_size", "Group size"), ("short_description", "Short description"), ("long_description", "Long description"), ("academic_credits", "Academic credits"), ("course_id", "Course ID"), ("course_name", "Course name")]
    return search_fields

def get_all_sortby_fields():
    '''Returns all fields that can be sorted by on projectlist page'''
    sortby_fields = [("start_date", "Start date"),("project_name", "Project name"), ("end_date", "End date"), ("group_size", "Group size"), ("academic_credits", "Academic credits"),("course_id", "Course ID"), ("course_name", "Course name")]
    return sortby_fields


def get_selected_techniques_for_search():
    '''Returns all techniques selected on the projectlist page.'''
    technique_list = get_all_techniques()

    selected_techniques = []

    for technique in technique_list:
        arg = get_request_args(technique)
        if arg[technique]:
            selected_techniques.append(arg[technique])

    return selected_techniques

def get_selected_fields_for_search():
    '''Returns all search fields selected on the projectlist page.'''
    search_fields = get_all_search_fields()
    selected_fields = []

    for field in search_fields:
        arg = get_request_args(field[0])
        if arg[field[0]]:
            selected_fields.append(arg[field[0]])

    return selected_fields

def get_selected_sortby_field_for_search():
    '''Returns the selected sort by field on the projectlist page.'''
    arg = get_request_args("sortby")
    return arg["sortby"]

def get_selected_sortorder_field_for_search():
    '''Returns the selected order for sorting the results on the projectlist
    page. If no order has been chosen, the default is descending.'''
    arg = get_request_args("sortorder")["sortorder"]

    if arg==None:
        arg = "desc"

    return arg


def get_projects_by_selected_techniques(selected_techniques):
    ''' Returns all projects from the default json database that used all
    techiques in the passed list of techniques. If the passed list is None all
    projects will be returned.'''
    db = get_data()
    return handledata.search(db, techniques = selected_techniques)


def get_author_data():
    '''Returns all data about the author/user of the portfolio.'''
    json_url = os.path.join(PROJECT_ROOT, 'author.json')
    return json.loads(open(json_url, encoding="utf-8").read())

def set_default_values(db):
    '''Looks for a valid image type in big_image and small_image in a database,
    and a valid image type is as long as the type name contains 3 to 4 letters.
    If there aren't a valid picture for a project a default image is set for the
     project. Otherwise a picture named after the project ID number is set. This
      only modifies a copy of the database and returns it. '''
    db_copy = copy.deepcopy(db)
    for project in db_copy:
        if not re.search("\w+\.\w{3,4}", project["big_image"]):
            project["big_image"] = "Programming-languages.jpg"
        else:
            project["big_image"] = "project" + str(project["project_id"]) + "/" + project["big_image"]

        if not re.search("\w+\.\w{3,4}", project["small_image"]):
            project["small_image"] = "No_image_available.svg"
        else:
            project["small_image"] = "project" + str(project["project_id"]) + "/" + project["small_image"]

        if not re.search("\w+\.\w{3,4}", project["project_image"]):
            project["project_image"] = "No_image_available.svg"
        else:
            project["project_image"] = "project" + str(project["project_id"]) + "/" + project["project_image"]

    return db_copy



# --- HTTP Related Functions ---

def get_request_args(*arg_names):
    '''Specific parameters from the GET or POST request can be extracted. The
    wanted parameter(s) are passed into the function, and the parameters with
    their values are returned in a dictionary.  Accepts any number of string
    values - one for each key.'''
    arg_table = {}
    if request.method == 'GET':
        for arg in arg_names:
            arg_table[arg] = request.args.get(arg)
    elif request.method == 'POST':
        for arg in arg_names:
            arg_table[arg] = request.form[arg]

    return arg_table



def form_value_add_item(form_value, item):
    '''Appends a string to a comma separated GET value string.
    X,Y -> X,Y,<item>.'''
    if item == None or len(item) == 0:
        return

    item_list = None
    if form_value == None or form_value == "":
        item_list = []
    else:
        item_list = form_value.split(',')

    if not item in item_list:
        item_list.append(item)

    return ','.join(item_list)

def form_value_remove_item(form_value, item):
    '''Removes a string from a comma separated GET value string.
    X,<item>,Y -> X,Y.'''
    if form_value == None or len(form_value) == 0:
        return ""

    item_list = form_value.split(',')
    item_list.remove(item)

    return ','.join(item_list)

# --- Style Functions --

techniques_decorative_wing_pairs = [('<', '>'), ('(', ')'), ('[', ']'),
                                    ('{', '}'), ('/', '/'), ('.', '.'),
                                    ('%', '%')]

def assign_random_wing_pair_to_technique_list(technique_list):
    '''Iterates a list of technique dictionaries and adds a set of matching
    characters to each dictionary with the keys 'left_wing' and 'right_wing'.'''
    if technique_list == None or len(technique_list) == 0:
        return

    # Create a list with indices 0 to length of technique_list.
    index_to_decorative_wings = [i for i in range(len(technique_list))]
    # Randomize this list.
    randomize_list(index_to_decorative_wings)

    # Transform each element in technique_list.
    for i in range(len(technique_list)):
        # Assign each element a random pair of "wings".
        wing_pair = techniques_decorative_wing_pairs[index_to_decorative_wings[i] % len(techniques_decorative_wing_pairs)]

        #decoration_map[technique_list[i]] = wing_pair
        technique_list[i]['left_wing'] = wing_pair[0]
        technique_list[i]['right_wing'] = wing_pair[1]


# --- Super Generic Help Functions ---
import random

def randomize_list(lst):
    '''Iterates a list and swaps each element with another element at a random
    position in the list. The passed list is transformed!'''
    if lst == None or len(lst) <= 1:
        return

    random.seed()
    for i in range(len(lst)):
        random_index = random.randint(0, len(lst) - 1)
        if random_index != i:
            lst[i], lst[random_index] = lst[random_index], lst[i]




if __name__ == "__main__":
    app.run(debug=True)
