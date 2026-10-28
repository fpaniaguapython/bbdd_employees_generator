

from pathlib import Path
import sys
import random 
import database_generator as db_gen

NAMES_FILE_NAME = 'nombres.txt'
SURNAMES_FILE_NAME = 'apellidos.txt'
JOB_CATEGORIES_FILE = 'categorias_profesionales.txt'
PROVINCIAS_FILE_NAME = 'provincias.txt'
COMUNIDADES_AUTONOMAS_FILE_NAME = 'comunidades_autonomas.txt'
EMPLOYEES_NUMBER = 1_000
MIN_SALARY = 10_000
MAX_SALARY = 100_000
MISSING_PROVINCE_PERCENTAGE = 0.1 # Porcentaje de empleados que no tendrán provincia asignada

class Person:
    def __init__(self, name: str, surname1: str, surname2: str, job_category: str, salary: float, province: str):
        self.name = name
        self.surname1 = surname1
        self.surname2 = surname2
        self.job_category = job_category
        self.salary = salary
        self.province = province
        
    def __str__(self):
        return f"{self.name} {self.surname1} {self.surname2}, {self.job_category}, {self.salary:.2f}"

def read_names(file_name: str) -> list:
    with open(file_name, mode='r', encoding='utf-8') as file:
        name_list = file.readlines()
    return [name.strip() for name in name_list]

def read_surnames(file_name: str) -> list:
    with open(file_name, mode='r', encoding='utf-8') as file:
        surname_list = file.readlines()
    return [name.strip() for name in surname_list]

def read_job_categories(file_name: str) -> list:
    with open(file_name, mode='r', encoding='utf-8') as file:
        job_list = file.readlines()
    return [job.strip() for job in job_list]

def read_comunidades_autonomas(file_name: str) -> list:
    with open(file_name, mode='r', encoding='utf-8') as file:
        comunidades_autonomas = file.readlines()
    return [job.strip() for job in comunidades_autonomas]

def read_provincias(file_name: str) -> list:
    with open(file_name, mode='r', encoding='utf-8') as file:
        provincias = file.readlines()
    return [job.strip().split(',') for job in provincias]

if __name__=='__main__':
    # Antes de comenzar, se elimina la base de datos si existe y se pregunta al usuario si desea continuar
    deletion_approved = input(f"Si existe, se va a eliminar el fichero {db_gen.DATABASE_NAME}. ¿Está seguro? (s/n): ")
    if deletion_approved.lower() != 's':
        sys.exit(0)

    try:
        # Borrado el fichero de base de datos
        file = Path(db_gen.DATABASE_NAME     )
        file.unlink()
    except FileNotFoundError:
        print('No se ha encontrado el fichero de base de datos, se creará uno nuevo.')
    else:
        print(f'Fichero {db_gen.DATABASE_NAME} eliminado correctamente.')

    # Obtención de los datos de los ficheros
    names = read_names(NAMES_FILE_NAME)
    surnames = read_surnames(SURNAMES_FILE_NAME)
    job_categories = read_job_categories(JOB_CATEGORIES_FILE)
    comunidades_autonomas = read_comunidades_autonomas(COMUNIDADES_AUTONOMAS_FILE_NAME)
    provincias = read_provincias(PROVINCIAS_FILE_NAME)


    # Generate and store autonomous communities and provinces in the database
    db_gen.generate_comunidades_autonomas(comunidades_autonomas)
    db_gen.generate_provincias(provincias)

    # Generate Person instances and store them in the database
    provincias = db_gen.get_provincias()
    employees = []
    for _ in range(EMPLOYEES_NUMBER):
        if random.random() < MISSING_PROVINCE_PERCENTAGE:
            province=None
        else:
            province=random.choice(provincias)[0]
                    
        person = Person(
            name=random.choice(names),
            surname1=random.choice(surnames),
            surname2=random.choice(surnames),
            job_category=random.choice(job_categories),
            salary=int(random.randint(MIN_SALARY, MAX_SALARY)),
            province=province
        )
        employees.append(person)

    db_gen.generate_employees(employees)

    # Generate unknown provinces
    unknown_provinces = [('Desconocida', None), ('No especificada', None), ('Sin asignar', None)]
    db_gen.generate_provincias(unknown_provinces)


    
    