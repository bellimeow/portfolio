##TEST##

from os import system
import handledata

from handledata import get_project_count


def automated_test(db):
    #system("clear")

    project_count = handledata.get_project_count(db)
    print("get_project_count(db): ", project_count)
    print("Get project names and ids using get_project:")
    for i in range(project_count):
        project = handledata.get_project(db, i)
        if project:
            try:
                print_project(project, as_list_item = True)
            except Exception:
                print("\t* The project with ID: {} is either invalid or you did something wrong (Yes, you!).")
        else:
            print("\t* No project with the ID: {} exists (Don't worry it's okay).".format(i))

    all_techniques = handledata.get_techniques(db)
    print("Get all techniques used (get_techniques):")
    for item in all_techniques:
        print("\t* ", item)

    all_technique_stats = handledata.get_technique_stats(db)
    print("Get all techniques and the projects that use them (get_technique_stats):")
    for k, v in all_technique_stats.items():
        print("\tTechnique: ", k)
        for item in v:
            print("\t\t* ID: {}, Name: {}".format(item['id'], item['name']))

def interactive_test(db):
    #system("clear")



    while True:

        print("What would you like to test? Type Q to quit.")
        print("\t1. get_project")
        print("\t2. search")
        c = input("Select one: ")

        if c == 'Q' or c == 'q':
            break
        elif c == '1':
            interactive_test_get_project(db)
        elif c == '2':
            interactive_test_search(db)
        else:
            print()
            print("Here's your test - spell this backwards:")
            print("\tDAER OT NRAEL")
            answer = input("What does it say?: ")
            if answer == "LEARN TO READ":
                print("Good job.")
                print()

def interactive_test_get_project(db):
    while True:
        c = input("Type the ID of a project to display or Q to quit: ")
        if c == 'Q' or c == 'q':
            break

        try:
            c = int(c)
        except Exception:
            continue

        project = handledata.get_project(db, c)
        if project:
            try:
                print_project(project, include_all_info = True)

            except Exception:
                print("\t* The project with ID: {} is either invalid or you have done something wrong (Yes, you!).")
        else:
            print("\t* No project with the ID: {} exists (Don't worry it's okay).".format(i))

def interactive_test_search(db):
    while True:
        sort_by = input("Sort by: ")

        sort_order = input("Sort order? (A)scending or (d)escending: ")
        if sort_order == 'A' or sort_order == 'a':
            sort_order = 'asc'
        elif sort_order == 'D' or sort_order == 'd':
            sort_order = 'desc'
        else:
            print("I don't have time for this...")
            sort_order = 'asc'

        techniques = input("Techniques to search for (separated by , or empty to ignore techniques completely): ").split(',')
        if len(techniques) == 0 or techniques[0] == '':
            techniques = None

        search = input("Search: ")
        search_fields = input("Search field (leave empty to search all fields): ").split(',')
        if len(search_fields) == 0:
            search_fields = None

        print("sort_by = {}, sort_order = {}, techniques = {}, search = {}, search_field = {}".format(sort_by, sort_order, techniques, search, search_fields))
        search_results = handledata.search(db, sort_by, sort_order, techniques, search, search_fields)

        if len(search_results) == 0 or search_results[0] == '':
            print("Too bad! We didn't find your search. Buhu..")

        for project in search_results:
            print_project(project, as_list_item = True)

def print_project(project, as_list_item = False, include_all_info = False, tabs = 1):
    print("{}{}ID: {}".format('\t' * tabs, "* " if as_list_item == True else "", project['project_id']))
    print("{}{}Name: {}".format('\t' * tabs, "  " if as_list_item == True else "", project['project_name']))

    if include_all_info:
        techniques_used = project.get('techniques_used', None)
        if techniques_used:
            print("{}{}Techniques used:".format('\t' * tabs, "  " if as_list_item == True else ""))
            for item in techniques_used:
                print(('\t' * tabs) + "\t* ", item)

        print("Misc project stats:".format('\t' * tabs, "  " if as_list_item == True else ""))
        exclude_keys = ['project_id', 'project_name', 'techniques_used']
        for k, v in project.items():
            if not k in exclude_keys:
                print(('\t' * tabs) + "\t* {}: {}".format(k, v))



print("-- handledata tests --")

db = handledata.load('data.json')

c = input("Run interactive test? (Y/N): ")
if c == 'Y' or c == 'y':
    interactive_test(db)
elif c == 'N' or c == 'n':
    automated_test(db)
else:
    print()
    print("You're stupid. I'm not gonna do error checks just because you can't read!")
    print()
