import os
import sys
import unittest
import importlib.util
from fastapi.testclient import TestClient

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

task1_module = load_module("task1_app", "task1_fastapi/main.py")
task2_module = load_module("task2_app", "task2_flask/app.py")
sys.path.insert(0, os.path.abspath("task5_integration"))
task5_module = load_module("task5_app", "task5_integration/main.py")


class TestTask1FastAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(task1_module.app)

    def test_01_root_welcome(self):
        """1. GET / - Return a welcome message"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        print("[PASS] Task 1: GET / - Welcome message passed.")

    def test_02_get_students(self):
        """2. GET /students - Return list of students"""
        response = self.client.get("/students")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        print(f"[PASS] Task 1: GET /students - Retrieved {len(data)} students.")

    def test_03_get_student_by_id(self):
        """3. GET /students/{id} - Return details of student"""
        response = self.client.get("/students/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], 1)
        self.assertIn("name", data)
        self.assertIn("email", data)
        print("[PASS] Task 1: GET /students/1 - Details verified.")

    def test_04_post_student(self):
        """4. POST /students - Add a new student"""
        payload = {
            "name": "Tanvi Joshi",
            "email": "tanvi.joshi@example.com",
            "course": "B.Tech CSE",
            "marks": 91.5
        }
        response = self.client.post("/students", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["name"], payload["name"])
        self.assertEqual(data["email"], payload["email"])
        self.assertIn("id", data)
        print(f"[PASS] Task 1: POST /students - Added student with ID #{data['id']}.")

    def test_05_delete_student(self):
        """5. DELETE /students/{id} - Delete a student"""
        response = self.client.delete("/students/1")
        self.assertEqual(response.status_code, 200)
        # Verify 404 on subsequent get
        get_res = self.client.get("/students/1")
        self.assertEqual(get_res.status_code, 404)
        print("[PASS] Task 1: DELETE /students/1 - Deleted and verified 404.")


class TestTask2Flask(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        task2_module.app.config["TESTING"] = True
        cls.client = task2_module.app.test_client()

    def test_01_home_page(self):
        """1. Home Page renders with welcome message and links"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("Welcome to the Student Portal", html)
        self.assertIn("Student List", html)
        print("[PASS] Task 2: Home Page loaded with navigation links.")

    def test_02_student_list_page(self):
        """2. Student List Page renders table with student details"""
        response = self.client.get("/students")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("<table", html)
        self.assertIn("Aarav Sharma", html)
        print("[PASS] Task 2: Student List Page renders table with students.")

    def test_03_add_student_get_and_post(self):
        """3. Add Student Form GET & POST"""
        # GET form
        response = self.client.get("/students/add")
        self.assertEqual(response.status_code, 200)
        self.assertIn("<form", response.data.decode("utf-8"))

        # POST form
        post_data = {
            "name": "Manish Kumar",
            "email": "manish.kumar@example.com",
            "course": "B.Tech IT",
            "marks": "87.5"
        }
        res_post = self.client.post("/students/add", data=post_data, follow_redirects=True)
        self.assertEqual(res_post.status_code, 200)
        self.assertIn("Manish Kumar", res_post.data.decode("utf-8"))
        print("[PASS] Task 2: Add Student form submission (POST) successful.")

    def test_04_student_details_page(self):
        """4. Student Details Page renders complete profile"""
        response = self.client.get("/students/2")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("Diya Patel", html)
        self.assertIn("Student Profile", html)
        print("[PASS] Task 2: Student Details Page renders successfully.")

    def test_05_bonus_search(self):
        """Bonus: Search students by name"""
        response = self.client.get("/students?search=Diya")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("Diya Patel", html)
        print("[PASS] Task 2: Bonus Search functionality verified.")


# 3. Test Task 5 (Integration with PostgreSQL & SQLAlchemy)
class TestTask5Integration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(task5_module.app)

    def test_01_root(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        print("[PASS] Task 5: Root health endpoint OK.")

    def test_02_create_and_get_students(self):
        payload = {
            "name": "Integration Test Student",
            "email": "auto_test_unique@example.com",
            "course": "B.Tech CSE",
            "marks": 93.5
        }
        res = self.client.post("/students", json=payload)
        self.assertIn(res.status_code, [201, 400])

        res_list = self.client.get("/students")
        self.assertEqual(res_list.status_code, 200)
        self.assertIsInstance(res_list.json(), list)
        print(f"[PASS] Task 5: POST & GET /students returned {len(res_list.json())} students.")

    def test_03_update_student(self):
        res_list = self.client.get("/students")
        first_id = res_list.json()[0]["id"]
        res = self.client.put(f"/students/{first_id}", json={"marks": 97.0})
        self.assertEqual(res.status_code, 200)
        print(f"[PASS] Task 5: PUT /students/{first_id} updated marks successfully.")


if __name__ == "__main__":
    unittest.main()
