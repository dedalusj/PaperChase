#!kuws/bin/python
from keepupwithscience import api

app = api.create_app()
app.run(debug = True)