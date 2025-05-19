# pip install ortools
from ortools.sat.python import cp_model
import json
from collections import namedtuple

# Charger les données JSON
with open('subjects.json', 'r', encoding='utf-8') as f:
    subjects_data = json.load(f)

with open('rooms.json', 'r', encoding='utf-8') as f:
    rooms_data = json.load(f)

# Constantes
DAYS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
PERIODS = ["P1", "P2", "P3", "P4", "P5"]
PERIOD_WEIGHTS = {"P1": 5, "P2": 4, "P3": 3, "P4": 2, "P5": 1}  # + important le matin

model = cp_model.CpModel()

# Variables de décision: cours x salle x jour x période -> bool
Assignment = namedtuple("Assignment", ["class_name", "subject_code", "teacher", "room", "day", "period"])
all_vars = {}
assignments = []

# Collecte des données exploitables
for level, semestres in subjects_data['niveau'].items():
    for sem, info in semestres.items():
        class_id = f"N{level}S{sem}"
        for subject in info['subjects']:
            code = subject.get('code', 'UNKNOWN')
            raw_teachers = subject.get('Course Lecturer', ["", ""])
            teachers = [f"{nom.strip()} {prenom.strip()}".strip() for nom, prenom in zip(raw_teachers[::2], raw_teachers[1::2]) if nom.strip() or prenom.strip()]
            for teacher in teachers:
                for room in rooms_data['Informatique']:
                    room_id = room['num']
                    for day in DAYS:
                        for period in PERIODS:
                            key = (class_id, code, teacher, room_id, day, period)
                            var = model.NewBoolVar(f"x_{class_id}_{code}_{teacher}_{room_id}_{day}_{period}")
                            all_vars[key] = var
                            assignments.append((key, var))

# Contraintes

# 1. Un cours donné une seule fois par semaine
for level, semestres in subjects_data['niveau'].items():
    for sem, info in semestres.items():
        class_label = f"N{level}S{sem}"
        for subject in info['subjects']:
            code = subject.get('code', 'UNKNOWN')
            raw_teachers = subject.get('Course Lecturer', ["", ""])
            teachers = [f"{nom.strip()} {prenom.strip()}".strip() for nom, prenom in zip(raw_teachers[::2], raw_teachers[1::2]) if nom.strip() or prenom.strip()]
            for teacher in teachers:
                vars_for_course = [var for (k, var) in all_vars.items() if k[0] == class_label and k[1] == code and k[2] == teacher]
                model.Add(sum(vars_for_course) == 1)

# 2. Pas deux cours en même temps pour une classe
for level, semestres in subjects_data['niveau'].items():
    for sem in semestres:
        class_label = f"N{level}S{sem}"
        for day in DAYS:
            for period in PERIODS:
                vars_in_slot = [var for (k, var) in all_vars.items() if k[0] == class_label and k[4] == day and k[5] == period]
                model.Add(sum(vars_in_slot) <= 1)

# 3. Pas deux cours dans une même salle en même temps
for room in rooms_data['Informatique']:
    room_id = room['num']
    for day in DAYS:
        for period in PERIODS:
            vars_in_room = [var for (k, var) in all_vars.items() if k[3] == room_id and k[4] == day and k[5] == period]
            model.Add(sum(vars_in_room) <= 1)

# 4. Fonction objectif: maximiser les cours le matin
objective_terms = []
for (k, var) in all_vars.items():
    weight = PERIOD_WEIGHTS[k[5]]
    objective_terms.append(weight * var)
model.Maximize(sum(objective_terms))

# Résolution
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print("\n--- EMPLOI DU TEMPS ---\n")
    for (key, var) in all_vars.items():
        if solver.Value(var) == 1:
            class_id, code, teacher, room, day, period = key
            print(f"{day} {period}: {class_id} - {code} avec {teacher} en salle {room}")
else:
    print("Aucune solution trouvée.")
