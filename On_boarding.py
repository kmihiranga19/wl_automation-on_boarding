import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 5)

driver.get("https://worklenz.com/auth/signup")
driver.maximize_window()

fake = Faker()
task_names = ["Planning", "Designing", "Coding", "Testing", "Maintaining", "Release"]


def signUp():
    random_name = fake.name()
    random_email = fake.email()
    wait.until(EC.visibility_of_element_located((By.ID, "full-name"))).send_keys(random_name)
    wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(random_email)
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys("ceyDigital#00")
    form = driver.find_element(By.TAG_NAME, "form")
    sign_up = form.find_elements(By.TAG_NAME, "button")[0]
    sign_up.click()
    time.sleep(2)


def give_organization_name():
    random_org_name = fake.name()
    organization = random_org_name + " Team"
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "input"))).send_keys(organization)
    continue_btn = driver.find_element(By.TAG_NAME, "button")
    if continue_btn.is_enabled():
        continue_btn.click()
        time.sleep(2)
    else:
        print("Please enter valid organization name")
    return organization


def create_first_project():
    project = fake.random_element(elements=('A', 'B', 'C', 'D'))
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "input"))).send_keys(
        "First project" +
        project)
    input_element = driver.find_element(By.TAG_NAME, "input")
    first_project_name = input_element.get_attribute("value")
    continue_btn = driver.find_element(By.XPATH, "//span[normalize-space()='Continue']")
    continue_btn.click()
    time.sleep(5)
    return first_project_name


def create_first_tasks():
    add_another_task = driver.find_element(By.XPATH, "//span[normalize-space()='Add another']")
    continue_btn = driver.find_element(By.XPATH, "//span[normalize-space()='Continue']")

    i = 0

    while i < 5:
        add_another_task.click()
        i += 1

    time.sleep(3)

    for i in range(6):
        element = driver.find_element(By.ID, f"task-name-input-{i}")
        element.send_keys(task_names[i])

    time.sleep(2)
    continue_btn.click()


def invite_team_members():
    add_another_task = driver.find_element(By.XPATH, "//span[normalize-space()='Add another']")
    continue_btn = driver.find_element(By.XPATH, "//span[normalize-space()='Continue']")

    i = 0

    while i < 2:
        add_another_task.click()
        i += 1

    menu = driver.find_element(By.TAG_NAME, "nz-list")
    inputs = menu.find_elements(By.TAG_NAME, "input")

    for i in range(3):
        random_email = fake.email()
        inputs[i].send_keys(random_email)

    if continue_btn.is_enabled():
        continue_btn.click()
        time.sleep(3)

    else:
        print("Please enter valid Email address")

    time.sleep(10)


def skip_invite_team_members():
    skip_btn = driver.find_element(By.CSS_SELECTOR, "span[class='ant-typography']")
    skip_btn.click()


def get_organization_name():
    header = driver.find_element(By.TAG_NAME, "worklenz-header")
    header_div = header.find_elements(By.TAG_NAME, "div")[1]
    header_ul = header_div.find_elements(By.TAG_NAME, "ul")[1]
    team_selection = header_ul.find_elements(By.TAG_NAME, "li")[0]
    team_selection.click()
    time.sleep(1)
    team_selection_items = driver.find_element(By.CLASS_NAME, "align-items-baseline")
    team = team_selection_items.find_elements(By.TAG_NAME, "span")[0]
    organization_text = team.text.strip()
    return organization_text


def get_project_name():
    page_header_title = driver.find_element(By.TAG_NAME, "nz-page-header-title")
    project_title = page_header_title.find_element(By.CLASS_NAME, "project-title")
    project_text = project_title.text.strip()
    return project_text


def get_project_tasks():
    tasks = []
    task_rows = driver.find_elements(By.TAG_NAME, "worklenz-task-list-row")
    for task_row in task_rows:
        task_name = task_row.find_element(By.CLASS_NAME, "task-name-text")
        tasks.append(task_name.text.strip())

    return tasks


def check_organization_name(org_name, created_org_name):
    if created_org_name == org_name:
        print("Organization successfully created")

    else:
        print("Your entered organization not created")


def check_project_name(first_project_name, created_first_project_name):
    if created_first_project_name == first_project_name:
        print("First project successfully created")

    else:
        print("Your entered project not created")


def check_project_tasks(created_tasks):
    if len(task_names) == len(created_tasks):
        for created_task in created_tasks:
            if created_task in task_names:
                print(created_task + " task successfully created")

            else:
                print(created_task + " task not created")


signUp()
organization_name = give_organization_name()
project_name = create_first_project()
create_first_tasks()
invite_team_members()

created_organization_name = get_organization_name()
created_project_name = get_project_name()
created_tasks_name = get_project_tasks()
get_project_tasks()

check_organization_name(organization_name, created_organization_name)
check_project_name(project_name, created_project_name)
check_project_tasks(created_tasks_name)
