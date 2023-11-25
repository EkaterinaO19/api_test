import requests
import uuid

ENDPOINT = 'https://todo.pixegami.io'


def test_can_call_endpoint():
    resp = requests.get(ENDPOINT)
    assert resp.status_code == 200


def test_can_create_task():
    payload = new_task_payload()

    create_task_resp = create_task(payload)
    assert create_task_resp.status_code == 200

    data = create_task_resp.json()
    print(data)

    task_id = data["task"]["task_id"]
    get_task_resp = get_task(task_id)
    assert get_task_resp.status_code == 200

    get_task_data = get_task_resp.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]


def test_can_update_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    new_payload = { 
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "my task 2",
        "is_done": True,
        }
    
    update_task_resp = update_task(new_payload)
    assert update_task_resp.status_code == 200

    get_task_resp = get_task(task_id)
    assert get_task_resp.status_code == 200
    get_task_data = get_task_resp.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]

    pass


def test_can_list_tasks():
    n = 3
    payload = new_task_payload()

    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    user_id = payload["user_id"]
    list_task_resp = list_tasks(user_id)
    assert list_task_resp.status_code == 200
    data = list_task_resp.json()

    tasks = data["tasks"]
    assert len(tasks) == n
    print(f"Number of tasks: {len(tasks)}")
    print(f"Expected number of tasks: {n}")
    print(data)

def test_delete_task():
    payload = new_task_payload()

    create_task_resp = create_task(payload)
    assert create_task_resp.status_code == 200
    task_id = create_task_resp.json()["task"]["task_id"]


    delete_task_resp = delete_task(task_id)
    assert delete_task_resp.status_code == 200

    get_deleted_task = get_task(task_id)
    assert get_deleted_task.status_code == 404



# helpers func
def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)

def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"my task_{uuid.uuid4().hex}"

    print(f"Create task for user {user_id} with content {content}")

    return {
        "content": content,
        "user_id": user_id,
        "is_done": False,
    }

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")