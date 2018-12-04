# Webpage portfolio

A web portfolio that is generated dynamically based on data files. The data files contain information about the owner of the portfolio, and about the projects that are to be displayed.

## Instructions for installation
To set up the portfolio system, it is necessary to ensure that Python3, pip, git and Flask ist installed. The installation procedures for these are explained in the [installation manual](project_documents/ind_installationsmanual/ind_installationsmanual.tex). 

The repository for the portfolio can then be cloned. Using the terminal, navigate to the folder where you would like to place the cloned repository, and execute the following command:

```
$ git clone https://gitlab.ida.liu.se/isade842/TDP003-Portfolio.git
```

Follow the instructions in the terminal to finish the cloning procedure.

The portfolio system can now be run on a server. To test it on a temporary development server supplied by Flask, execute the following command:

```
$ python3 myFlaskProject.py
```

## System folder structure
Below, the folder structure is shown. Note that only the most crucial files and folders are displayed. A closer description of the folders and files can be found in the [system documentation](project_documents/systemdokumentation/systemdokumentation.tex)

```
TDP003-portfolio/
    project_documents/
    static/
        images/
        style/
        scripts/
    templates/
    README.md
    ourdata.json
    author.json
    myFlaskProject.py
    handledata.py
```

## Basic usage
The information displayed on the portfolio webpage originate from two JSON-files that are placed in the root folder of the system, specifically ''author.json'' and ''ourdata.json''. These files can be changed, so that the information is tailored to the person using the portfolio as his or her own.

### author.json
The file ''author.json'' contains the information about the owner that is to be shown on the portfolio. It is built similar to a python dictionary. It's original content is the following:

```
{
    "name": "",
    "photo": "",
    "profession": "",
    "email": "",
    "social_media":
        {
        "twitter": "",
        "github": "",
        "codepen": "",
        "linkedin": "",
        "instagram": "",
        "facebook": "",
        "gitlab": ""
        },
    "about_me": ""
}
```

The owner can enter his or her own information in the file. The social media information should consist of a link to the owner's account on that particular platform. Importantly, new social media platforms should only be entered after looking up the wanted [Font Awesome icon](http://fontawesome.io/icons/), and using that icon's name as the dictionary key in ''author.json''.

### ourdata.json
The file ''ourdata.json'' contains information about all projects that are to be displayed on the portfolio. It is structured similar to a list of dictionaries, where each dictionary represents a project. New projects can be added by adding and filling in a new such project dictionary.

The project dictionary is structured the following way:

```
{
    "start_date": "",
    "short_description": "",
    "course_name": "",
    "long_description": "",
    "group_size": 0,
    "academic_credits": "",
    "lulz_had": "",
    "external_link": "",
    "small_image": "",
    "techniques_used": [],
    "project_name": "Portfolio",
    "course_id": "",
    "end_date": "",
    "project_id": 1,
    "big_image": ""
}
```

All values can be left blank except for project_id, which must a a unique integer, and project name. More information about the fields can be found in the [system documentation](project_documents/systemdokumentation/systemdokumentation.tex).

More detailed information about how author and project images should be treated can be found in the [images README file](static/images/README.txt).
 
## Further development
The portfolio system may be changed and adapted according to the owner's needs and wishes. For help in the development process, the [system documentation](project_documents/systemdokumentation/systemdokumentation.tex) should be consulted.



# How to install virtualenv
1. "virtualenv -p python3 <virtualenvname>"
2. "source bin/activate"
3. "pip install Flask"
4. And start your flask module, 
	"python3 <flaskmodule>.py"
5. To deactivate your virtualenvironment,
	"deactivate"
