from modules.app import app
from modules.router import Router
from modules.containers.home import home

router = Router()
router.register_callbacks(app)
router.route("/")(home)

if __name__ == "__main__":
    app.run_server(debug=True)