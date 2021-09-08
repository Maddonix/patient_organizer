#
attributes = [
    "Antikoagulation",
    "Antibiose",
    "L. gerichtet",
    "L. gesichtet",
    "Intervention",
    "Physio",
    "Sozial",
    "Ernährung" 
]

def patient_default_dict():
    _dict = {_: {
            "state": False,
            "comment": None,
        } for _ in attributes}

    return _dict