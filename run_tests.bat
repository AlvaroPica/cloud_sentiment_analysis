:: -v   increase verbosity.
:: -s   shortcut for --capture=no (to allow prints inside tests)
cls && pytest -v -s -k "not test_merge"
:: TODO because file write is not mocked, test_merge must be executed last
pytest -v -s -k "test_merge"

