from termgraph import termgraph as tg


def test_normalize_returns_correct_results():
    expected = [
        [18.00891997563707],
        [22.715484213214925],
        [1.6140440497475292],
        [4.932510757019078],
        [50.0],
        [20.83128671630941],
        [0.09823761714835845],
    ]
    results = tg.normalize(
        [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [1.0]], 50
    )
    assert results == expected


def test_normalize_with_all_zeros_returns_correct_results():
    expected = [
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
    ]
    results = tg.normalize([[0], [0], [0], [0], [0], [0], [0]], 50)
    assert results == expected


def test_normalize_with_negative_datapoint_returns_correct_results():
    expected = [
        [18.625354066709058],
        [23.241227816636798],
        [2.546389964737846],
        [5.8009133475923464],
        [50.0],
        [21.393336801741913],
        [0.0],
    ]
    results = tg.normalize(
        [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [-10.0]], 50
    )
    assert results == expected


def test_normalize_with_larger_width_does_not_normalize():
    data = [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [1.0]]
    expected = [
        [7203.567990254828],
        [9086.193685285969],
        [645.6176198990117],
        [1973.0043028076311],
        [20000.0],
        [8332.514686523764],
        [39.29504685934338],
    ]
    results = tg.normalize(data, 20000)
    assert results == expected