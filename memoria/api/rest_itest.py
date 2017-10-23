import unittest
import json
import urllib3

# -------------------------------------------------------------------------------------------------
# test fact rest api - fixtures


fact_rq_1 = {"owner": "temple", "labels": ["multiplication"], "question": "1 x 2", "answer": "2"}
fact_rq_2 = {"owner": "temple", "labels": ["multiplication"], "question": "2 x 2", "answer": "4"}
fact_rq_3 = {"owner": "temple", "labels": ["multiplication"], "question": "2 x 3", "answer": "6"}
fact_rq_ne = {"uuid": "non-existent-uuid", "owner": "temple", "labels": ["multiplication"],
              "question": "2 x 4", "answer": "8"}


# -------------------------------------------------------------------------------------------------
# test fact rest api - tests


class TestFactRESTAPI(unittest.TestCase):

    def test_add_fact(self):
        rest_client = FactRESTAPIClient()
        rest_client.clean_all_facts()

        status, new_fact = rest_client.create_fact(fact_rq_2)
        self.assertEqual(status, 201)
        self.assertIsNotNone(new_fact["uuid"])
        self.assertIsNotNone(new_fact["created_at"])
        self.assertIsNotNone(new_fact["modified_at"])
        self.assertEqual(new_fact["owner"], "temple")
        self.assertEqual(new_fact["labels"], ["multiplication"])
        self.assertEqual(new_fact["question"], "2 x 2")
        self.assertEqual(new_fact["answer"], "4")
        rest_client.clean_all_facts()

    def test_list_facts(self):
        rest_client = FactRESTAPIClient()
        rest_client.clean_all_facts()

        rest_client.create_fact(fact_rq_1)
        rest_client.create_fact(fact_rq_2)
        rest_client.create_fact(fact_rq_3)

        status, facts = rest_client.list_facts()
        self.assertEqual(status, 200)
        self.assertIsNotNone(facts, None)
        self.assertEqual(facts['page'], 1)
        self.assertEqual(facts['pages'], 1)
        self.assertEqual(facts['per_page'], 10)
        self.assertEqual(facts['total'], 3)
        self.assertEqual(len(facts['items']), 3)
        rest_client.clean_all_facts()

    def test_get_fact(self):
        rest_client = FactRESTAPIClient()
        rest_client.clean_all_facts()

        rest_client.create_fact(fact_rq_1)
        _, target_fact = rest_client.create_fact(fact_rq_2)
        rest_client.create_fact(fact_rq_3)

        status, retrieved_fact = rest_client.get_fact(target_fact['uuid'])
        self.assertEqual(status, 200)
        self.assertIsNotNone(retrieved_fact["uuid"])
        self.assertIsNotNone(retrieved_fact["created_at"])
        self.assertIsNotNone(retrieved_fact["modified_at"])
        self.assertEqual(retrieved_fact["owner"], "temple")
        self.assertEqual(retrieved_fact["labels"], ["multiplication"])
        self.assertEqual(retrieved_fact["question"], "2 x 2")
        self.assertEqual(retrieved_fact["answer"], "4")
        rest_client.clean_all_facts()

    def test_get_non_exististent_fact(self):
        rest_client = FactRESTAPIClient()
        rest_client.clean_all_facts()

        status, error_fact = rest_client.get_fact('non-existent-uuid')
        self.assertEqual(status, 404)
        self.assertEqual(error_fact["message"],
                         "The fact 'non-existent-uuid' could not be found.")
        rest_client.clean_all_facts()

    def test_update_fact(self):
        rest_client = FactRESTAPIClient()
        rest_client.clean_all_facts()

        rest_client.create_fact(fact_rq_1)
        _, target_fact = rest_client.create_fact(fact_rq_2)
        rest_client.create_fact(fact_rq_3)

        target_fact["labels"] = ["multiplication", "maths"]
        target_fact["question"] = "6 x 6"
        target_fact["answer"] = "36"
        status, _ = rest_client.update_fact(target_fact)
        _, updated_fact = rest_client.get_fact(target_fact['uuid'])
        self.assertEqual(status, 204)
        self.assertIsNotNone(updated_fact["uuid"])
        self.assertIsNotNone(updated_fact["created_at"])
        self.assertIsNotNone(updated_fact["modified_at"])
        self.assertEqual(updated_fact["owner"], "temple")
        self.assertEqual(updated_fact["labels"], ["multiplication", "maths"])
        self.assertEqual(updated_fact["question"], "6 x 6")
        self.assertEqual(updated_fact["answer"], "36")
        rest_client.clean_all_facts()

    def test_update_non_exististent_fact(self):
        rest_client = FactRESTAPIClient()
        rest_client.clean_all_facts()

        status, error_fact = rest_client.update_fact(fact_rq_ne)
        self.assertEqual(status, 404)
        self.assertEqual(error_fact["message"],
                         "The fact 'non-existent-uuid' could not be found. Unable to update fact.")
        rest_client.clean_all_facts()

    def test_delete_fact(self):
        rest_client = FactRESTAPIClient()
        rest_client.clean_all_facts()

        rest_client.create_fact(fact_rq_1)
        _, target_fact = rest_client.create_fact(fact_rq_2)
        rest_client.create_fact(fact_rq_3)

        status, _ = rest_client.delete_fact(target_fact['uuid'])
        self.assertEqual(status, 200)
        _, facts = rest_client.list_facts()
        self.assertIsNotNone(facts, None)
        self.assertEqual(facts['total'], 2)
        self.assertEqual(len(facts['items']), 2)
        rest_client.clean_all_facts()

    def test_delete_non_exististent_fact(self):
        rest_client = FactRESTAPIClient()
        rest_client.clean_all_facts()

        status, error_fact = rest_client.delete_fact('non-existent-uuid')
        self.assertEqual(status, 404)
        self.assertEqual(error_fact["message"],
                         "The fact 'non-existent-uuid' could not be found. Unable to delete fact.")
        rest_client.clean_all_facts()


# -------------------------------------------------------------------------------------------------
# test fact rest api - support


class FactRESTAPIClient():

    http = urllib3.PoolManager()
    # host = 'localhost:8888'
    host = 'localhost:8888'
    log = False

    def create_fact(self, fact):
        url = 'http://' + self.host + '/api/fact/facts/'
        response = self.http.request('POST', url,
                                     headers={'Content-Type': 'application/json'},
                                     body=json.dumps(fact))
        if self.log:
            log_response(response)
        return (response.status, json.loads(response.data))

    def list_facts(self):
        url = 'http://' + self.host + '/api/fact/facts/?page=1&per_page=10'
        response = self.http.request('GET', url,
                                     headers={'Accepts': 'application/json'})
        if self.log:
            log_response(response)
        return (response.status, json.loads(response.data))

    def get_fact(self, fact_uuid):
        url = 'http://' + self.host + '/api/fact/facts/' + fact_uuid
        response = self.http.request('GET', url,
                                     headers={'Accepts': 'application/json'})
        if self.log:
            log_response(response)
        return (response.status, json.loads(response.data))

    def update_fact(self, fact):
        url = 'http://' + self.host + '/api/fact/facts/' + fact['uuid']
        response = self.http.request('PUT', url,
                                     headers={'Content-Type': 'application/json',
                                              'Accepts': 'application/json'},
                                     body=json.dumps(fact))
        if self.log:
            log_response(response)
        if response.data is not None and response.data is not b'':
            return (response.status, json.loads(response.data))
        else:
            return (response.status, None)

    def delete_fact(self, fact_uuid):
        url = 'http://' + self.host + '/api/fact/facts/' + fact_uuid
        response = self.http.request('DELETE', url,
                                     headers={'Content-Type': 'application/json'})
        if self.log:
            log_response(response)
        if response.data is not None and response.data is not b'':
            return (response.status, json.loads(response.data))
        else:
            return (response.status, None)

    def clean_all_facts(self):
        _, fact_list = self.list_facts()
        facts = fact_list['items']
        for fact in facts:
            self.delete_fact(fact['uuid'])


def log_response(response):
    print("http status  : ", response.status)
    print("http headers : ", response.headers)
    print("http data    : ", response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
