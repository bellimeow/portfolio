import json



def load(filename):
    '''Loads a file and returns a list of all the projects sorted by project
    id:s.'''
    try:
        with open(filename, encoding="utf-8") as data_file:
            data = json.load(data_file)

            # Sort the projects by project id.
            sorted_data = sorted(data, key = lambda k: k['project_id'])
            return sorted_data
    except:
        return None




def get_project_count(db):
    '''Returns the number of the total projects in a list. '''
    return len(db)



def get_project(db, id):
    '''Returns the project specified by the project id.'''
    for project in db:
        if id == project['project_id']:
            return project

    return None



def get_techniques(db):
    '''Returns a sorted list of all techniques used in all projects.'''
    all_techniques = []

    for project in db:
        techniques_used = project.get('techniques_used', None)
        if techniques_used:
            for technique in techniques_used:
                if technique not in all_techniques:
                    all_techniques.append(technique)

    return sorted(all_techniques)



def get_technique_stats(db):
    '''Returns a dictionary containing techniques and the projects in which they
     are used. The projects are represented only by their id and name.'''
    technique_stats = {}

    for project in db:
        # For each project we insert information about the project's id and
        # name.
        project_info = {'id': project['project_id'],
                        'name': project['project_name']}

        techniques_used = project.get('techniques_used', None)
        if techniques_used:
            for technique in techniques_used:
                if technique not in technique_stats:
                    technique_stats[technique] = []

                technique_stats[technique].append(project_info)

    return technique_stats



def search(db, sort_by = 'start_date', sort_order = 'desc', techniques = None,
            search = None, search_fields = None):
    '''Returns a list of projects that have a field that contains the specified
    user input and sort by any field, either ascending or descending. Defaults
    to sorting by start date. If search_fields is None, then all the projects
    fields are searched and returned.'''
    matching_projects = []

    # If search is None then return all projects.
    if search == None:
        search = ""

    search = search.lower()

    # First find all matching projects.
    for project in db:
        if search_in_project(project, techniques, search, search_fields):
            matching_projects.append(project)

    # Finally sort the projects.
    return sort_projects(matching_projects, sort_by, sort_order)



'''
The functions below are not a part of the API.
'''



def search_in_project(project, techniques, search, search_fields):
    '''Searches a specific project for techniques or content.'''
    if techniques:
        # Check if project_techniques contains all techniques in techniques.
        project_techniques = project['techniques_used']
        for technique in techniques:
            if technique not in project_techniques:
                return False

    if isinstance(search_fields, list) and len(search_fields) == 0:
        # If list of search fields are empty (but not None!), no search can be
        # done
        return False
    elif not search_fields:
        return recursive_search_object(project, search)
    else:
        # Check for search in each of the search fields. If any of fields
        # contain the search string, return True.
        for search_field in search_fields:
            project_field = project.get(search_field, None)
            if search_field != None and
                recursive_search_object(project_field, search):
                return True

    return False



def recursive_search_object(obj, search):
    '''Recursively searches any object, if object is a container then it's
    children will be searched instead.'''

    if isinstance(obj, (tuple, list, dict)):
        # If object is a dict, ignore it's keys.
        if isinstance(obj, dict):
            obj = obj.values()

        for list_item in obj:
            if recursive_search_object(list_item, search):
                return True

        return False

    # If the object happens to be an integer or other non-string type, then
    # convert it to a string and search it.
    return search in str(obj).lower()



def sort_projects(db, sort_by, sort_order):
    '''Returns a list of all the projects sorted by a specified field and in a
    specified order.'''

    sort_descending = sort_order == 'desc'

    # '\uffff' is default key when sorted by ascending.
    # \uffff represents the highest possible unicode character.
    # '\u0000' is default key when sorted by descending.
    # \u0000 represents the lowest possible unicode character.
    missing_key = '\u0000' if sort_descending else '\uffff'

    # If the search field is not present in the project then always sort it
    # last.
    return sorted(db, key = lambda k: k[sort_by] if sort_by in k else
                  missing_key, reverse = sort_descending)
