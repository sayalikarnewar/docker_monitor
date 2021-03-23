from views import monitor

# URL Routes for rest server
def routes(app):
    app.router.add_get("/", monitor)