:: -v   increase verbosity.
:: -s   shortcut for --capture=no (to allow prints inside tests)
cls && pytest -v -s -k "not test_analyze"
:: TODO because file write is not mocked, test_analyze must be executed last
pytest -v -s -k "test_analyze"

