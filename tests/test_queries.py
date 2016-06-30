from nose.tools import eq_
from conceptnet5.query import AssertionFinder

test_finder = None


def setUp():
    global test_finder
    test_finder = AssertionFinder(
        'testdata/index/assertions.index',
        'testdata/assertions/assertions.msgpack'
    )


def test_lookup():
    quiz1 = list(test_finder.lookup('/c/en/quiz'))
    eq_(len(quiz1), 3)

    quiz2 = list(test_finder.lookup('/c/en/quiz', offset=1))
    eq_(quiz2, quiz1[1:])

    quiz3 = list(test_finder.lookup('/c/en/quiz', limit=2))
    eq_(quiz3, quiz1[:2])

    verbosity_test = quiz1[0]
    eq_(verbosity_test['start'], '/c/en/test')
    eq_(verbosity_test['end'], '/c/en/quiz')
    eq_(verbosity_test['rel'], '/r/RelatedTo')
    eq_(verbosity_test['uri'], '/a/[/r/RelatedTo/,/c/en/test/,/c/en/quiz/]')
    eq_(verbosity_test['license'], 'cc:by/4.0')
    source = verbosity_test['sources'][0]
    eq_(source['contributor'], '/s/resource/verbosity')
    eq_(source['process'], '/s/process/split_words')
    eq_(source['@id'], '/and/[/s/process/split_words/,/s/resource/verbosity/]')


def get_query_ids(query):
    return [match['@id'] for match in test_finder.query(query)]


def test_query_en_quiz():
    q1 = get_query_ids({'start': '/c/en/test', 'end': '/c/en/quiz'})
    testquiz = [
        '/a/[/r/RelatedTo/,/c/en/test/,/c/en/quiz/]',
        '/a/[/r/Synonym/,/c/en/test/n/,/c/en/quiz/]',
        '/a/[/r/Synonym/,/c/en/test/n/wikt/en_1/,/c/en/quiz/]'
    ]
    eq_(q1, testquiz)
    q2 = get_query_ids({'node': '/c/en/quiz'})
    eq_(q2, testquiz)


def test_query_en_form():
    q = get_query_ids({'rel': '/r/FormOf', 'end': '/c/en/test'})
    eq_(q, ['/a/[/r/FormOf/,/c/en/tests/,/c/en/test/n/]'])


def test_query_es():
    q = get_query_ids({'start': '/c/en/test', 'end': '/c/es'})
    eq_(q, ['/a/[/r/Synonym/,/c/en/test/n/wikt/en_1/,/c/es/prueba/]'])


def test_query_source():
    q = get_query_ids({'node': '/c/en/test', 'source': '/s/resource/jmdict/1.07'})
    eq_(q, ['/a/[/r/Synonym/,/c/ja/テスト/n/,/c/en/test/]'])