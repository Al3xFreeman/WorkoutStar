from datetime import datetime
from turtle import title
from flask import current_app, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.main.forms import EditProfileForm, EmptyForm, ExerciseForm, PostForm
from app import db
from app.main import bp
from app.models import Exercise, Sesion, User

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        
        #post = Post(body=form.post.data, author=current_user)
        #db.session.add(post)
        db.session.commit()
        flash('Your post is now published!')
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    #posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    #Ternary operator
    #next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    #prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None

    #return render_template("index.html", title='Home', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)
    return "Hola"

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    #posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    #next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
    #prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None

    #return render_template("index.html", title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)
    sesions = Sesion.query.order_by(Sesion.date.desc()).all()
    return render_template("all_sesions.html", title='Explore sesions', sesions=sesions)


@bp.route('/explore/sesions')
@login_required
def explore_sesions():
    page = request.args.get('page', 1, type=int)
    #posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    #next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
    #prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None

    #return render_template("index.html", title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)
    sesions = Sesion.query.order_by(Sesion.date.desc()).all()
    return render_template("all_sesions.html", title='Explore sesions', sesions=sesions)


@bp.route('/sesion/<sesion_id>', methods=['GET', 'POST'])
def sesion(sesion_id):
    exerciseForm = ExerciseForm()
    sesion = Sesion.query.get_or_404(sesion_id)

    if exerciseForm.validate_on_submit():
        exercise = Exercise(sesion=sesion, name=exerciseForm.name.data)
        db.session.add(exercise)
        db.session.commit()
        flash("Eexercise added succesfully")
        return redirect(url_for('main.sesion', sesion_id = sesion_id))

    return render_template('sesion_info.html', title="Sesion info", sesion=sesion, form=exerciseForm)

@bp.route('/sesion/<sesion_id>/exercises')
def sesion_exercises(sesion_id):
    sesion_exercises = Sesion.query.get_or_404(sesion_id).exercises.all()

    return render_template('exercises_sesion.html', title="Exercises in Sesion: " + str(sesion_id), exercises=sesion_exercises, sesion_id = sesion_id)


@bp.route('/user/<username>')
@login_required
def user(username):
    form = EmptyForm()
    
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    #posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)

    #next_url = url_for('main.user', username=user.username, page=posts.next_num) if posts.has_next else None
    #prev_url = url_for('main.user', username=user.username, page=posts.prev_num) if posts.has_prev else None

    #return render_template('user.html', user=user, posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)
    return render_template('user.html', user=user)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data

        db.session.commit()
        flash('Your changes have been saved')

        return redirect(url_for('main.edit_profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    
    return render_template('edit_profile.html', title = 'Edit Profile', form = form)
