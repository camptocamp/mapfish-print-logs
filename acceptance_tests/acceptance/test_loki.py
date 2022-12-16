from mapfish_print_logs.loki import escape


def test_escape():
    assert escape("11'22") == "11'22"
    assert escape('11"22') == r"11\"22"
    assert escape(r"11\22") == r"11\\22"
