import os, json, boto3, pytest
from moto import mock_aws
from nature_island_service.handler import handler


@pytest.fixture(autouse=True)
def _env():
    os.environ["AWS_REGION"] = "eu-west-1"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"
    os.environ["TABLE_NAME"] = "dom_items"
    yield


@mock_aws
def test_end_to_end_get_post_get():
    ddb = boto3.client("dynamodb", region_name="eu-west-1")
    ddb.create_table(
        TableName="dom_items",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    # bad input -> 400
    r_bad = handler({"httpMethod": "POST", "body": json.dumps({"name": " ", "location": ""})}, None)
    assert r_bad["statusCode"] == 400

    # empty list -> 200
    r0 = handler({"httpMethod": "GET"}, None)
    assert r0["statusCode"] == 200
    assert json.loads(r0["body"])["items"] == []

    # create -> 201
    r1 = handler({"httpMethod": "POST", "body": json.dumps({
        "name": "Boiling Lake", "location": "Morne Trois Pitons"
    })}, None)
    assert r1["statusCode"] == 201

    # list now has at least 1 item
    r2 = handler({"httpMethod": "GET"}, None)
    assert r2["statusCode"] == 200
    assert len(json.loads(r2["body"])["items"]) >= 1
