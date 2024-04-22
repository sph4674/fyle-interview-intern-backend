from flask import Blueprint, request
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from core.libs import helpers
from core.apis import decorators
from core.apis.decorators import authenticate_principal
from core.apis.responses import APIResponse
from core import db  

principal_bp = Blueprint('principal', __name__)


@principal_bp.route('/assignments', methods=['GET'])
@decorators.authenticate_principal
def list_assignments(principal):
    assignments = Assignment.get_assignments_by_principal()
    assignment_data = [
        {
            'id': assignment.id,
            'student_id': assignment.student_id,
            'teacher_id': assignment.teacher_id,
            'content': assignment.content,
            'grade': assignment.grade,
            'state': assignment.state,
            'created_at': assignment.created_at.isoformat(),
            'updated_at': assignment.updated_at.isoformat()
        }
        for assignment in assignments
    ]
    return APIResponse.respond(data=assignment_data)


@principal_bp.route('/teachers', methods=['GET'])
@decorators.authenticate_principal
def list_teachers(principal):
    teachers = Teacher.query.all()
    teacher_data = [
        {
            'id': teacher.id,
            'user_id': teacher.user_id,
            'created_at': teacher.created_at.isoformat(),
            'updated_at': teacher.updated_at.isoformat()
        }
        for teacher in teachers
    ]
    return APIResponse.respond(data=teacher_data)


@principal_bp.route('/assignments/grade', methods=['POST'])
@decorators.authenticate_principal
def grade_assignment(principal):
    data = request.json
    assignment_id = data.get('id')
    grade = data.get('grade')

    if not assignment_id or not grade:
        return APIResponse.respond(error='Assignment ID and grade are required', status_code=400)

    assignment = Assignment.get_by_id(assignment_id)
    if not assignment:
        return APIResponse.respond(error='Assignment not found', status_code=404)

    assignment.grade = grade
    assignment.state = 'GRADED'
    assignment.updated_at = helpers.get_utc_now()

    try:
        db.session.commit()
    except Exception as e:
        return APIResponse.respond(error=str(e), status_code=500)

    return APIResponse.respond(data={
        'id': assignment.id,
        'student_id': assignment.student_id,
        'teacher_id': assignment.teacher_id,
        'content': assignment.content,
        'grade': assignment.grade,
        'state': assignment.state,
        'created_at': assignment.created_at.isoformat(),
        'updated_at': assignment.updated_at.isoformat()
    })
