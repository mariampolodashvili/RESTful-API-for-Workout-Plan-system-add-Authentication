from db import db


class ExercisePlanModel(db.Model):
    __tablename__ = "exercise_plans"

    id = db.Column(db.Integer, primary_key=True)
    repetitions = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    distance = db.Column(db.Float, nullable=True)
    exercise=db.Column(db.String, nullable=True)


    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), unique=False, nullable=False)
    plan = db.relationship("PlanModel", back_populates="exercise_plans")


    # exercises = db.relationship("ExerciseModel", back_populates="exercise_plan", cascade="all, delete-orphan")



