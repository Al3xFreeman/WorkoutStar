# WorkoutStar
Workout manager and routine generator service


This is how the system is intended to work:
- A user can perform any exercise that is registered as a valid exercise in the ExerciseDef table
- Every exercise is part of a Session. A Session can just have one exercise.
- Exercises have attached a GoalExercise, it represents the goal for the user to perform.
- Exercises can have several Sets, that data will be used to compare it against the GoalExercise
- Sessions can belong to a Workout. A Workout is comprised of one or several sessions.
- Sessions can also belong directly to the user, as standalone exercise performed.
- Workouts are assigned to routines. It represents a series of sessions (and thus, exercises) to be performed at a certain day and time.
- Routines are assigned to users (and customizable).

- Sessions that belong to Workouts (and Routines) will have the option to create non-done exercises (with the field "done" = False) and add information to the GoalExercise model. That way the user will be able to see all forecoming sessions/workouts and the exercises left to do inside them.
