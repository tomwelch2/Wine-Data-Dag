import unittest
from airflow.models import DagBag, TaskInstance
from airflow.utils.dates import days_ago
from airflow import DAG

class TestDag(unittest.TestCase):
    def setUp(self):
        self.dags = DagBag()

    def test_task_numbers(self):
        task = self.dags.get_dag("wineDataDag")
        self.assertEqual(len(task.tasks), 6)


if __name__ == "__main__":
    unittest.main()
