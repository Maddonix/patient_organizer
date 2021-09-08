import pandas as pd
from pathlib import Path
from datetime import datetime as dt
from datetime import date as date
from collections import defaultdict
from utils import patient_default_dict
import json
import os

PATH_PATIENTS = Path("data")

# Patient Class is more like a interface between a dataframe storing the patients and an easy to work with object to handle individual patients
class Patient:
    def __init__(self, path = None, name = None):
        if path:
            with open(path, "r") as f:
                self.data = json.load(f)
            self.path = path
        else:
            assert name
            self.data = defaultdict(patient_default_dict)["BJÖÖÖÖÖÖÖÖRN"]
            new_path = PATH_PATIENTS.joinpath(name).with_suffix(".json")
            self.path = new_path
            if new_path.exists():
                pass
            else:
                self.save()

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f)

    def reset(self):
        for attribute in self.data.keys():
            self.data[attribute]["state"] = False
        self.save()

    def get_attribute_states(self):
        # Returns list of touples [(attribute_name, attribute_state), ...]
        return [(name, values["state"]) for name, values in self.data.items()]

    def get_attribute_comments(self):
        # Returns list of touples [(attribute_name, attribute_comment), ...]
        return [(name, values["comment"]) for name, values in self.data.items()]

    def set_attribute_states(self, attribute_dict):
        # Expects dict {attribute_name: attribute_state, ...}
        for key, value in attribute_dict.items():
            self.data[key]["state"] = value
        self.save()


class Organizer:
    def __init__(self):
        self.refresh()
        # self.df = self.patients_to_dataframe()

    def load_patients(self, path_patients:Path = PATH_PATIENTS):
        patient_json_paths = [_ for _ in path_patients.iterdir() if _.suffix == ".json"]
        patients = {_.with_suffix("").name: Patient(_) for _ in patient_json_paths}
        patient_data = {}
        for pat_name, pat_obj in patients.items():
            patient_data[pat_name] = {_: __["state"] for _, __ in pat_obj.data.items()}
        df = pd.DataFrame.from_dict(patient_data).T

        return patients, df

    def delete_patient(self, key):
        path = PATH_PATIENTS.joinpath(key).with_suffix(".json")
        if path.exists():
            os.remove(path)

    def get_patient_attribute_states(self, key):
        patient = self.patients[key]
        return patient.get_attribute_states()

    def set_patient_attribute_states(self, key, attribute_dict):
        patient = self.patients[key]
        patient.set_attribute_states(attribute_dict)
        self.refresh()

    def refresh(self):
        self.patients, self.df = self.load_patients(PATH_PATIENTS)

    def reset(self):
        for pat_name, pat_object in self.patients.items():
            pat_object.reset()
        self.patients, self.df = self.load_patients(PATH_PATIENTS)



    # def patients_to_dataframe(self):
        # _df_dict = {}
        # for patient_path, patient in self.patients.items():
        #     attributes = []
        #     print(patient.data)
        #     for attribute, value in patient.data.items():
        #         if attribute == "Name":
        #             pass
        #         else:
        #             attributes.append(value["state"])
                
        #     _df_dict[patient.data["Name"]] = attributes
        # pat_data = {}
        # for key, value in self.patients.items()
        # return pd.DataFrame().from_dict("patiet")#.from_dict(self.patients)
