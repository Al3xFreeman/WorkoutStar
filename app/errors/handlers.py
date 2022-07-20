from flask import render_template
from app import db
from app.errors import bp

@bp.app_errorhandler(404)
def not_found_error(error):
    print("a")
    return render_template('404.html'), 404


@bp.app_errorhandler(500)
def internal_erorr(error):
    print("b")
    return render_template('500.html'), 500