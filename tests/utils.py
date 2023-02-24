from unittest.mock import MagicMock


def get_mock_response(status_code=200, json={}):
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = json
    return response


get_project_response = {
    "name": "foo",
    "collections": ["my-collection"],
    "groups": {
        "read": [
            "admin",
        ]
    },
    "client_id": "foobar",
    "created_at": "2022-12-16T00:33:39.893305+00:00",
    "updated_at": "2023-02-17T14:40:49.394311+00:00",
}

get_policies_for_collection_response = [
    {
        "name": "check-tags",
        "source_name": "csd-policies",
        "raw_policy": {
            "name": "check-tags",
            "description": "resources should be tagged",
            "resource": "terraform.aws_*",
            "metadata": {"severity": "HIGH"},
            "filters": [{"__tfmeta.type": "resource"}, {"tags.Environment": "absent"}],
        },
        "resource": "terraform.aws_*",
        "severity": "high",
        "created_at": "2022-12-14T19:11:18.528637+00:00",
        "updated_at": "2022-12-14T19:11:18.528637+00:00",
    }
]


create_scan_response = {
    "id": "278741d4-99a7-4ca7-80e2-1cbd49d8391b",
    "project_name": "foo",
    "status": "PASSED",
    "summary": {"HIGH": 0, "MEDIUM": 0, "LOW": 0},
    "trigger": "USER",
    "user_id": "foo@bar.com",
    "client_id": "none",
    "sort": 0,
    "created_at": "2023-02-23T00:28:53.921774+00:00",
}
