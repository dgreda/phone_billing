#!/usr/bin/env bash
set -e

trap error_handler ERR

# pretty colours
SET_BLACK_TEXT="\e[30m"
SET_YELLOW_TEXT="\e[33m"
SET_RED_BACKGROUND="\e[101m"
SET_ERROR_TEXT="$SET_BLACK_TEXT$SET_RED_BACKGROUND"
RESET_FORMATTING="\e[0m"
ERROR_PREFIX="${SET_ERROR_TEXT}ERROR:${RESET_FORMATTING}"

error_handler() {
  exitcode=$?
  echo -e "$SET_ERROR_TEXT $BASH_COMMAND failed!!! $RESET_FORMATTING"
  # Some more clean up code can be added here before exiting
  exit $exitcode
}

echo "Starting test suite..."

function run_steps() {
  echo "Running black..."
  # Source discovery is controlled by settings in pyproject.toml
  # A path to scan is required.
  eval "black --quiet ."

  echo "Running isort..."
  # Source discovery is controlled by settings in pyproject.toml
  # A path to scan is required.
  eval "isort ."

  echo "Running mypy..."
  # Source discovery is controlled by settings in mypy.ini
  # Specifying a path takes precedence over settings file.
  eval "mypy"

  echo "Running pytest..."
  # General test discovery is controlled by settings in pyproject.toml
  # The explicit path is used so a single pytest config can be used to unit and integration tests
  eval "pytest tests -vv"

  echo "Running flake8..."
  # Source discovery is controlled by settings in .flake8
  eval "flake8"

  echo "Running bandit..."
  # Source discovery is controlled by settings in .bandit
  # Explicitly specifying settings file because using a different path will cause the file to be ignored.
  eval "bandit --ini .bandit -rq ."
}

run_steps
