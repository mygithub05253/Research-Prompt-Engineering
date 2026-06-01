@echo off
python -m gic_v13.cli run tests\fixtures\request.yaml --fixture-dir tests\fixtures\opendart --output-dir outputs
echo.
echo Open outputs\fixture_cli_run\deliverables\preview.html
