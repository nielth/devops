import database


def test_match_user_id_with_note_id():
    assert database.match_user_id_with_note_id("1e3acedb82a9d9bdbd75723a3ea215059159fc21") == "TEST"
    assert database.match_user_id_with_note_id("1f90a08ac4e231db43a20905adf448dd42482230") == "ADMIN"


def test_read_note_from_db():
    assert database.read_note_from_db("TEST")[0]['note_id'] == "1e3acedb82a9d9bdbd75723a3ea215059159fc21"
    assert database.read_note_from_db("ADMIN")[0]['note_id'] == "1f90a08ac4e231db43a20905adf448dd42482230"
