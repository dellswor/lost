The files in this directory implement a very simple web application to take in and present user entered data.

The form on the welcome page submits to the goodbye page, which displays the data the user entered. If the expected data is missing, the goodbye page renders the index.htmltemplate instead of the goodbye template.

Note on the _bad_ design shown:
The design currently in this directory, while it works, does not follow best practices. The URL that presents a form should also be the action target for the form. This makes the web application much easier to maintain since the page responsible for the form is also responsible for parsing the form.

Redirects should be used to point the user to the correct next page after their input data has been processed; in both the success and failure cases.


Files:
app.py - A Flask app to be run via mod_wsgi
config.py - Logic to find and read the configuration into memory
lost_config.json - a sample configuration file
templates/
    index.html - a template for the root path
    welcome.html - a template for the welcome page
    goodbye.html - a template for the goodbye page
