from db import db

class ExerciseModel(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    descriptions = db.Column(db.String, unique=False, nullable=False)
    instructions = db.Column(db.String, unique=False, nullable=False)
    target_muscles = db.Column(db.String, unique=False, nullable=False)


    #
    # exercise_plan_id = db.Column(db.Integer, db.ForeignKey('exercise_plans.id'), unique=False, nullable=False)
    # exercise_plan = db.relationship("ExercisePlanModel",  back_populates="exercises")
    #
    #
    #
