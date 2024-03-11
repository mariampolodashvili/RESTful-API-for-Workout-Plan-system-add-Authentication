from flask.views import MethodView
from flask_smorest import Blueprint,abort
from flask_jwt_extended import jwt_required
from db import db
from models import PlanModel
from schemas import PlanSchema, UpdatePlan
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
blp=Blueprint("plans", __name__, description="operations on plans")


@blp.route("/plans/<int:plan_id>")
class Plan(MethodView):

    @jwt_required()
    @blp.response(200, PlanSchema)
    def get(self, plan_id):
        plan = PlanModel.query.get_or_404(plan_id)
        return plan

    def delete(self, plan_id):
        plan = PlanModel.query.get_or_404(plan_id)
        db.session.delete(plan)
        db.session.commit()
        return {"message": "Plan deleted"}


    @jwt_required()
    @blp.arguments(UpdatePlan)
    @blp.response(200, PlanSchema)
    def put(self, plan_data, plan_id):
        plan = PlanModel.query.get(plan_id)
        if plan:
            plan.name=plan_data['name']
            plan.goals=plan_data['goals']
            plan.workout_frequency = plan_data['workout_frequency']
            plan.daily_session_duration = plan_data['daily_session_duration']
        else:
            plan=PlanModel(id=plan_id, **plan_data)

        db.session.add(plan)
        db.session.commit()

        return plan



@blp.route("/plans")
class PlansList(MethodView):

    @jwt_required()
    @blp.response(200, PlanSchema(many=True))
    def get(self):
        return PlanModel.query.all()

    @jwt_required()
    @blp.arguments(PlanSchema)
    @blp.response(200, PlanSchema)
    def post(self, plan_data):
        plan=PlanModel(**plan_data)
        try:
            db.session.add(plan)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message = "A plan with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the plan")


        return plan