from api import create_app

def run():
    app, socket = create_app()
    socket.run(app, debug=True)
run()