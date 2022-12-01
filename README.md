# README

Ranked choice voting calculator for the 2023 code4lib Keynote Committee.

The expected input is a CSV download from a Google Forms multiple choice question. The script will:
* deduplicate votes, keeping only the most recent vote from a given email address;
* calculate two winners using the single transferable vote strategy.

## Setup
* Install poetry
* `poetry install`
* Download the Google forms data to `voting.csv`

## Run it:
* `poetry run python ranked_choice.py`

Election results will be printed to console.