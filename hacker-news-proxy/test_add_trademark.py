from text_modification import add_trademark


def test_add_trademark():
    # Тест на обработку строки без шестизначных слов
    assert add_trademark("Short test") == "Short test", "Should not modify strings without six-letter words"

    # Тест на обработку строки с одним шестизначным словом
    assert add_trademark("Python is great") == "Python™ is great", "Should add trademark after six-letter words"

    # Тест на обработку строки с несколькими шестизначными словами
    assert add_trademark("Tester shows results") == "Tester™ shows results", "Should add trademark after each six-letter word"

    # Тест на обработку строки с шестизначными словами и пунктуацией
    assert add_trademark("Tester, always delivers quickly.") == "Tester™, always delivers quickly.", "Should handle punctuation correctly"

    # Тест на неизменность строки без английских буквенных символов
    assert add_trademark("123456 !@#$%^") == "123456 !@#$%^", "Should not modify non-alphabetic characters"
