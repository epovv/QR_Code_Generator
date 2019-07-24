from .models import Course, Group, StudentsAll
from django.db.utils import IntegrityError
import random
from datetime import date, timedelta


first_name = ["Jay", "Jim", "Roy", "Axel", "Billy", "Charlie", "Jax", "Gina",
             "Paul", "Ringo", "Ally", "Nicky", "Cam", "Ari", "Trudie", "Cal",
             "Carl", "Lady", "Lauren", "Ichabod", "Arthur", "Ashley", "Drake",
             "Kim", "Julio", "Lorraine", "Floyd", "Janet", "Lydia", "Charles",
             "Pedro", "Bradley", "Aaron", "Abraham", "Adam", "Adrian", "Aidan",
            "Alan", "Albert", "Alejandro", "Alex", "Alexander", "Alfred",
             "Andrew", "Angel", "Anthony", "Antonio", "Ashton", "Austin",
             "Daniel", "David", "Dennis", "Devin", "Diego", "Dominic",
             "Donald", "Douglas", "Dylan", "Harold", "Harry", "Hayden",
             "Henry", "Herbert", "Horace", "Howard", "Hugh", "Hunter",
             "Malcolm", "Martin", "Mason", "Matthew", "Michael", "Miguel",
             "Miles", "Morgan"]

last_name = ["Barker", "Style", "Spirits", "Murphy", "Blacker", "Bleacher",
            "Rogers", "Warren", "Keller", "Smith", "Johnson", "Williams",
            "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez",
            "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez",
            "Moore", "Martin", "Jackson", "Thompson", "White", "Lopez", "Lee",
            "Gonzalez", "Harris", "Clark", "Lewis", "Robinson", "Walker",
            "Perez", "Hall", "Young", "Allen", "Sanchez", "Wright", "King",
            "Scott", "Green", "Baker", "Adams", "Nelson", "Hill", "Ramirez",
            "Campbell", "Mitchell", "Roberts", "Carter", "Phillips", "Evans",
            "Turner", "Torres", "Parker", "Collins", "Edwards", "Stewart",
            "Flores", "Morris", "Nguyen", "Murphy", "Rivera", "Cook", "Rogers",
            "Morgan", "Peterson", "Cooper", "Reed", "Bailey", "Bell", "Gomez",
            "Kelly", "Howard", "Ward", "Cox", "Diaz", "Richardson", "Wood",
            "Watson", "Brooks", "Bennett", "Gray", "James", "Reyes", "Cruz",
            "Hughes", "Price", "Myers", "Long", "Foster", "Sanders", "Ross",
            "Morales", "Powell", "Sullivan", "Russell", "Ortiz", "Jenkins",
            "Gutierrez", "Perry", "Butler", "Barnes", "Fisher", "Henderson",
            "Coleman", "Simmons", "Patterson", "Jordan", "Reynolds",
            "Hamilton", "Graham", "Kim", "Gonzales", "Alexander", "Ramos",
            "Wallace", "Griffin", "West", "Cole", "Hayes", "Chavez", "Gibson",
            "Bryant", "Ellis", "Stevens", "Murray", "Ford", "Marshall",
            "Owens", "McDonald", "Harrison", "Ruiz", "Kennedy", "Wells",
            "Alvarez", "Woods", "Mendoza", "Castillo", "Olson", "Webb",
            "Washington", "Tucker", "Freeman", "Burns", "Henry", "Vasquez",
            "Snyder", "Simpson", "Crawford", "Jimenez", "Porter", "Mason",
            "Shaw", "Gordon", "Wagner", "Hunter", "Romero", "Hicks", "Dixon",
            "Hunt", "Palmer", "Robertson", "Black", "Holmes", "Stone", "Meyer",
            "Boyd", "Mills", "Warren", "Fox", "Rose", "Rice", "Moreno",
            "Schmidt", "Patel", "Ferguson", "Nichols", "Herrera", "Medina",
            "Ryan", "Fernandez", "Weaver", "Daniels", "Stephens", "Gardner",
            "Payne", "Kelley", "Dunn", "Pierce", "Arnold", "Tran", "Spencer",
            "Peters", "Hawkins", "Grant", "Hansen", "Castro", "Hoffman",
            "Hart", "Elliott", "Cunningham", "Knight", "Bradley"]

group_name = ['MTS-11', 'MTS-21', 'MTS-31', 'MTS-41', 'VM-11', 'VM-21',
              'VM-31', 'VM-41', 'SS-11', 'SS-21', 'SS-31', 'SS-41', 'IS-11',
              'IS-21', 'IS-31', 'IS-41']

course_name = ['Python', 'JavaScript', 'PHP']

def run_random():
    """Генератор случайных имен и активности"""
    for course in course_name:
        c = None
        try:
            c = Course.objects.create(course_name=course)
            c.save()
        except IntegrityError:
            print('База сгенерирована отключите скрипт')
        for i in range(random.randrange(2, 5)):
            a = None
            try:
                group = course + str(random.randrange(1, 100))
                a = Group.objects.create(
                    group_name=group,
                    course=c,
                    start_date=date.today(),
                    end_date=date.today() + timedelta(days=random.randrange(10, 30))
                )
                a.save()
            except IntegrityError:
                pass
            for i in range(random.randrange(10, 15)):
                if random.randrange(0, 100) > 95:
                    activity = False
                else:
                    activity = True
                name = random.choice(first_name) + ' ' + random.choice(last_name)
                b = StudentsAll.objects.create(
                    name=name,
                    start_date=date.today() + timedelta(days=random.randrange(0, 3)),
                    activity=activity
                )
                b.save()
                b.my_group.add(a)
                b.save()
                print(name + ' ...OK')
    print('finish')
