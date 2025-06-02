from flask import render_template
from app import create_app, db

app = create_app()

@app.route("/")
def index():
    return render_template('api.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", debug=True)
