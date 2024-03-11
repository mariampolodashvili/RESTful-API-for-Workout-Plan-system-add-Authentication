from flask.views import MethodView
from flask_smorest import Blueprint,abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from db import db
from schemas import ExerciseSchema
from models import ExerciseModel
blp=Blueprint("Exercises", "exercises",  description="operations on exercises")


@blp.route("/exercise/<exercise_id>")
class Exercise(MethodView):
    @jwt_required()
    @blp.response(200, ExerciseSchema)
    def get(self, exercise_id):
        exercise=ExerciseModel.query.get_or_404(exercise_id)
        return exercise

    @jwt_required()
    def delete(self, exercise_id):
        exercise=ExerciseModel.query.get_or_404(exercise_id)
        db.session.delete(exercise)
        db.session.commit()
        return {"message": "Exercise is deleted"}



@blp.route("/exercises")
class ExerciseList(MethodView):

    @jwt_required()
    @blp.response(200, ExerciseSchema(many=True))
    def get(self):
        return ExerciseModel.query.all()



    @jwt_required(fresh=True)
    @blp.arguments(ExerciseSchema)
    @blp.response(201, ExerciseSchema)
    def post(self, exercise_data):
        exercise = ExerciseModel(**exercise_data)
        try:
            db.session.add(exercise)
            db.session.commit()

        except SQLAlchemyError:
            abort(500,
                  message = "An error occurred while inserting the item" )

        return exercise

