from core.models.assignments import AssignmentStateEnum, GradeEnum
import logging


def test_grade_assignment_successful(client, h_teacher_1):
    """
    Test grading a submitted assignment successfully
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": GradeEnum.A.value
        }
    )

    assert response.status_code == 200
    data = response.json['data']

    assert data['id'] == 1
    assert data['state'] == AssignmentStateEnum.GRADED.value
    assert data['grade'] == GradeEnum.A.value


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    Test grading a draft assignment (should fail)
    """ 
    logging.info("Attempting to grade a draft assignment")
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 2,
            "grade": GradeEnum.B.value
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_invalid_grade(client, h_teacher_1):
    """
    Test grading with an invalid grade (should fail)
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"  # Invalid grade
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_nonexistent_assignment(client, h_teacher_1):
    """
    Test grading a non-existent assignment (should fail)
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,  # Non-existent assignment ID
            "grade": GradeEnum.A.value
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_already_graded(client, h_teacher_1):
    """
    Test grading an assignment that is already graded (should fail)
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,  # Already graded assignment
            "grade": GradeEnum.B.value
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'
