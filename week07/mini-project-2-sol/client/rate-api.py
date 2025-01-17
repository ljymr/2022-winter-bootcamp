def get_rate(client_id):
    """
    would expect to return a float rate.

    :param client_id: string, e.g. 'client1'
    :return: float, e.g. 0.2
    """
    import requests
    response = requests.get("http://127.0.0.1:5000/rate/" + client_id)
    print(response)
    return float(response.content)


def upsert_client_rate(client_id, rate):
    import requests
    response = requests.post("http://127.0.0.1:5000/rate", json={"client_id": client_id, "rate": rate})  # what to post?


# -----------------------Here are tests for API ------------------------
# -------If you want we can any other file call the API functions-------
def test_get_rate():
    print(get_rate('client1'))
    assert get_rate('client1') == 0.2
    assert get_rate('client0') == 0.0


def test_upsert_rate():
    # test create
    upsert_client_rate("client0", 0.1)
    assert get_rate("client0") == 0.1

    # test update
    new_rate = get_rate("client1") + 0.1
    upsert_client_rate("client1", new_rate)
    assert get_rate('client1') == new_rate

    # reset
    upsert_client_rate("client0", 0)


# DO NOT DELETE
if __name__ == '__main__':
    test_get_rate()
    test_upsert_rate()
