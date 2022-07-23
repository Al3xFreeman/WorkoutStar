from datetime import datetime, timedelta
from turtle import title
from flask import current_app, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.main.forms import EditProfileForm, EmptyForm, ExerciseDefForm, ExerciseForm, PostForm, RoutineForm, SesionForm
from app import db
from app.main import bp
from app.models import Exercise, ExerciseDef, Routine, Session, User

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # form = PostForm()
    # if form.validate_on_submit():
        
    #     #post = Post(body=form.post.data, author=current_user)
    #     #db.session.add(post)
    #     db.session.commit()
    #     flash('Your post is now published!')
    #     return redirect(url_for('main.index'))

    # page = request.args.get('page', 1, type=int)
    #posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    # Ternary operator
    # next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    # prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    today = datetime.now().date()
    start_of_week = today

    routines = current_user

    week = [start_of_week + timedelta(days=i) for i in range(0, 7)]



    return render_template("index.html", title='Home', week=week, routines=routines)
    # return "Hola"

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    #posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    #next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
    #prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None

    #return render_template("index.html", title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)
    sesions = Session.query.order_by(Session.date.desc()).all()
    return render_template("explore.html", title='Explore sesions')


@bp.route('/explore/sesions', methods=['GET', 'POST'])
@login_required
def explore_sesions():
    page = request.args.get('page', 1, type=int)
    #posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    #next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
    #prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None

    #return render_template("index.html", title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)
    form = SesionForm(date=datetime.now())
    if form.validate_on_submit():
        sesion = Session(user=current_user, date=form.date.data, due_time=form.due_time.data)
        db.session.add(sesion)
        db.session.commit()
        flash('Your sesion has been successfully added')
        return redirect(url_for('main.explore_sesions'))

    sesions = Session.query.order_by(Session.date.desc()).all()
    return render_template("all_sesions.html", title='Explore sesions', sesions=sesions, form=form)

@bp.route('/explore/sesions/<routine_id>')
def sesions_in_routine(routine_id):
    sesions = Routine.query.get_or_404(routine_id).sesions.all()
    return render_template("all_sesions.html", sesions = sesions, routine_id=routine_id)

@bp.route('/explore/routines', methods=['GET', 'POST'])
def explore_routines():

    form = RoutineForm()
    if form.validate_on_submit():
        routine = Routine(user=current_user)

        db.session.add(routine)
        db.session.commit()
        flash('New routine added for {}'.format(current_user.username))
        return redirect(url_for('main.explore_routines'))

    routines = Routine.query.order_by(Routine.user_id.asc()).all()
    return render_template("all_routines.html", routines = routines, form=form)

@bp.route('/routines/<routine_id>')
def routine(routine_id):
    routine = Routine.query.get_or_404(routine_id)

    return render_template('routine_info.html')

@bp.route('/sesions/<sesion_id>', methods=['GET', 'POST'])
def sesion(sesion_id):
    exerciseForm = ExerciseForm()
    sesion = Session.query.get_or_404(sesion_id)

    if exerciseForm.validate_on_submit():
        exercise = Exercise(sesion=sesion, name=exerciseForm.name.data)
        db.session.add(exercise)
        db.session.commit()
        flash("Eexercise added succesfully")
        return redirect(url_for('main.sesion', sesion_id = sesion_id))

    return render_template('sesion_info.html', title="Session info", sesion=sesion, form=exerciseForm)

@bp.route('/sesion/<sesion_id>/exercises')
def sesion_exercises(sesion_id):
    sesion_exercises = Session.query.get_or_404(sesion_id).exercises.all()

    return render_template('exercises_sesion.html', title="Exercises in Session: " + str(sesion_id), exercises=sesion_exercises, sesion_id = sesion_id)


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


@bp.route('/explore/user_exercises', methods=['GET', 'POST'])
def user_exercises():
    form = ExerciseForm()

    if form.validate_on_submit():
        ex = Exercise(name = form.name.data)
        session = Session.query.get(form.session_id.data)
        session.exercises.append(ex)
        exerciseDef = ExerciseDef.query.get(form.exercise_def_id.data)
        exerciseDef.exercises.append(ex)

        db.session.add(ex)
        db.session.add(session)
        db.session.add(exerciseDef)
        db.session.commit()

        flash("New user done exercise added to the database")

        return redirect(url_for('main.user_exercises'))

    exercises = Exercise.query.all()

    return render_template('all_user_exercises.html', title="User Exercises List", form = form, exercises = exercises, links = True)

@bp.route('/explore/user_exercises/<user_exercise_id>')
def user_exercises_info(user_exercise_id):
    ex = Exercise.query.get_or_404(user_exercise_id)
    if ex.session is not None:
        user = ex.session.user
    else:
        user = None

    return render_template('exercise_info.html', title="{} Info".format(ex.name), exercise = ex, user = user)


@bp.route('/explore/exercises', methods=['GET', 'POST'])
def exercises():
    form = ExerciseDefForm()

    if form.validate_on_submit():
        ex = ExerciseDef(name = form.name.data)
        db.session.add(ex)
        db.session.commit()

        flash("New exercise added to the database")

        return redirect(url_for('main.exercises'))

    exercises = ExerciseDef.query.all()

    return render_template('all_exercises.html', title="Exercises List", form = form, exercises = exercises, links = True)


@bp.route('/explore/exercises/<exercise_id>')
def exercise_info(exercise_id):
    exerciseDef = ExerciseDef.query.get_or_404(exercise_id)
    #user_exercises = exercise.exercises.join(Session).filter(User.username == current_user.username).all()
    user_exercises = exerciseDef.exercises.join(Session).join(User).all()
    
    total_weight = 0
    total_reps = 0
    
    for ex in user_exercises:
        for set in ex.sets:
            total_weight += set.weight
            total_reps += set.reps

    return render_template('exerciseDef_info.html', title="{} Info".format(exerciseDef.name), exerciseDef=exerciseDef, exercises = user_exercises, total_reps = total_reps, total_weight = total_weight)