from flask.views import MethodView
from flask_smorest import Blueprint,abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from flask import json
from db import db
from schemas import PlanExerciseSchema,UpdatePlanExerciseSchema
from models import ExercisePlanModel, ExerciseModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
blp=Blueprint("ExercisePlanModel", "exercise_plans", description="Operation on exercises plans")



@blp.route("/exercise_plan/<int:exercise_plan_id>")
class ExercisePlan(MethodView):

    @jwt_required()
    @blp.response(200, PlanExerciseSchema)
    def get(self, exercise_plan_id):
        exercise_plan = ExercisePlanModel.query.get_or_404(exercise_plan_id)
        return exercise_plan

    @jwt_required()
    def delete(self,exercise_plan_id ):
        exercise_plan_id= ExercisePlanModel.query.get_or_404(exercise_plan_id)
        db.session.delete(exercise_plan_id)
        db.session.commit()
        return {"message": "Exercise Plan deleted"}

    @jwt_required()
    @blp.arguments(UpdatePlanExerciseSchema)
    @blp.response(200, UpdatePlanExerciseSchema)
    def put(self, exercise_plan_data, exercise_plan_id):
        exersice_plan = ExercisePlanModel.query.get(exercise_plan_id)
        if exersice_plan:
            exersice_plan.repetitions = exercise_plan_data['repetitions']
            exersice_plan.sets = exercise_plan_data['sets']
            exersice_plan.duration = exercise_plan_data['duration']
            exersice_plan.distance = exercise_plan_data['distance']
        else:
            exersice_plan = ExercisePlanModel(id=exercise_plan_id, **exercise_plan_data)

        db.session.add(exersice_plan)
        db.session.commit()

        return exersice_plan



@blp.route("/exercise_plans")
class ExercisePlansList(MethodView):
    @jwt_required()
    @blp.response(200, PlanExerciseSchema(many=True))
    def get(self):
        return ExercisePlanModel.query.all()


@blp.route("/exercise_plans/<int:exercise_id>")
class PostExercisePlan(MethodView):

    @jwt_required()
    @blp.arguments(PlanExerciseSchema)
    @blp.response(200, PlanExerciseSchema)
    def post(self, exercise_plan_data, exercise_id):
        exercise_data = db.session.query(ExerciseModel).get(exercise_id)

        exercise_json = json.dumps({
            'name': exercise_data.name,
            'descriptions': exercise_data.descriptions,
            'instructions': exercise_data.instructions,
            'target_muscles': exercise_data.target_muscles
        })

        exercise_plan = ExercisePlanModel(
            repetitions=exercise_plan_data['repetitions'],
            sets=exercise_plan_data['sets'],
            duration=exercise_plan_data['duration'],
            distance=exercise_plan_data['distance'],
            exercise=str(json.loads(exercise_json)),
            plan_id=exercise_plan_data['plan_id']
        )

        try:
            db.session.add(exercise_plan)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message = "A exercise plan with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the exercise plan")

        return exercise_plan