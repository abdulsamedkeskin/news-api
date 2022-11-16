from api import create_app

def run():
    create_app().run(debug=True)
run()