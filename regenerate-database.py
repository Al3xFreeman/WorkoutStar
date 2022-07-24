from app import db, create_app
from app.models import *
import random
from config import Config
from datetime import datetime

class Regenerate(object):
    number_mock_users = 0
    number_routines = 0
    number_workouts = 0
    number_sessions = 0
    number_exerciseDef = 0
    number_exercises = 0
    number_sets = 0
    ex_names = ['Push Ups', 'Pull Ups', 'Sit Ups', 'Lunges', 'Squat', 'Leg Press', 'Deadlift', 'Leg Curl', 'Bench Press']

    def __init__(self, seed = 42, b_name = "user{}", b_email = "{}@test-email.com", b_pass = "test"):
        self.seed = seed
        self.base_username = b_name
        self.base_email = b_email
        self.base_password = b_pass
        random.seed(seed)

    def add_users(self, amount=10):
        self.number_mock_users = amount
        for i in range(amount):
            print(i)
            username = self.base_username.format(i)
            email = self.base_email.format(username)
            u = User(username = username, email=email)
            u.set_password(self.base_password)

            db.session.add(u)
            db.session.commit()

    def add_routines(self, amount=10):
        self.number_routines = amount
        for i in range(amount):
            mock_user_id = random.randint(0, self.number_mock_users - 1)
            
            u = User.query.filter_by(username=self.base_username.format(mock_user_id)).first()
            routine = Routine(period=random.randint(7,30))

            u.routines.append(routine)
            
            db.session.add(routine)
            db.session.commit()
            print(self.base_username.format(mock_user_id) + " has Routine ID:" + str(routine.id))

    def add_workouts(self, amount=20):
        self.number_workouts = amount
        for i in range(amount):
            routine_id = random.randint(1, self.number_routines)

            r = Routine.query.get(routine_id)
            workout = Workout(day=random.randint(0,7), name="Test Workout {}".format(i))

            r.workouts.append(workout)

            db.session.add(workout)
            db.session.commit()

            print("Routine {} has Workout {}".format(r.id, workout.id))


    def add_sessions(self, amount=50):
        self.number_sessions = amount
        tick = True
        for i in range(amount):
            session = Session(date = datetime.utcnow())

            if tick: #One session goes to a workout
                workout_id = random.randint(1, self.number_workouts)
                w = Workout.query.get(workout_id)
                w.sessions.append(session)

                w.routine.user.sessions.append(session)
                

            else: #Another one directly to the user
                user_id = random.randint(1, self.number_mock_users)
                u = User.query.get(user_id)

                u.sessions.append(session)

            db.session.add(session)
            db.session.commit()

            print("Session {} added to ".format(session.id) + ("Workout {}".format(w.id) if tick else "User {}".format(u)))

            if tick:
                tick = False
            else:
                tick = True

    def add_exercisesDef(self, amount=5):
        min_amount = min(len(self.ex_names), amount)
        self.number_exerciseDef = min_amount
        for i in range(min_amount):
            exDef = ExerciseDef(name=self.ex_names[i])
            db.session.add(exDef)
            db.session.commit()

            print("Exercise deefinition added with name {}".format(exDef.name))
        

    def add_exercises(self, amount=200):
        self.number_exercises = amount
        for i in range(amount):
            session_id = random.randint(1, self.number_sessions)
            exerciseDef_id = random.randint(1, self.number_exerciseDef)
            exercise_done = random.randint(0,1)
            s = Session.query.get(session_id)
            e_def = ExerciseDef.query.get(exerciseDef_id)
            exercise = Exercise(name="test", done=exercise_done, session=s, exercise_def=e_def, timestamp=datetime.utcnow(), duration=random.randint(0,60))

            db.session.add(exercise)
            db.session.commit()

            print("Exercise {}, was added to Session {}, performed by: {}".format(e_def.name, s.id, s.user.username))
        pass

    def add_sets(self, amount=300):
        self.number_sets = amount
        for i in range(amount):
            ex_id = random.randint(1, self.number_exercises)
            e = Exercise.query.get(ex_id)
            weight = random.randint(1,50)
            reps = random.randint(3,15)
            set = Set(weight=weight, reps=reps, exercise=e)

            db.session.add(set)
            db.session.commit()

            print("added set with {} kg and {} reps to exercise {} (with id: {}). It now has {} sets".format(set.weight, set.reps, set.exercise.exercise_def.name, set.exercise.id, set.exercise.sets.count()))
        pass


    def start(self):
        print("Starting")
        app = create_app(Config)
        app_context = app.app_context()
        app_context.push()
        db.session.remove()
        db.drop_all()
        db.create_all()

        self.add_users()
        self.add_routines()
        self.add_workouts()
        self.add_sessions()
        self.add_exercisesDef()
        self.add_exercises()
        self.add_sets()

        app_context.pop()

if __name__ == '__main__':
    regen = Regenerate()
    regen.start()