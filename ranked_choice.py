import copy
import csv
import subprocess

from pyrankvote import Candidate, Ballot, single_transferable_vote


def _remove_duplicates():
    names_already_seen = set()

    with open('voting.csv', 'r', encoding='utf-8') as infile:
        with open('deduped_voting.csv', 'a', encoding='utf-8') as outfile:
            csvfile = csv.DictReader(infile)

            out_fields = copy.copy(csvfile.fieldnames)
            out_fields.remove('Timestamp')
            out_fields.remove('Username')
            writer = csv.DictWriter(outfile, out_fields)

            writer.writeheader()

            for row in reversed(list(csvfile)):
                if row['Username'] in names_already_seen:
                    continue

                names_already_seen.add(row['Username'])
                writer.writerow({k: row[k] for k in out_fields})


def _raw_votes():
    with open('deduped_voting.csv', 'r', encoding='utf-8') as f:
        csvfile = csv.DictReader(f)

        candidate_names = copy.copy(csvfile.fieldnames)

        candidates = [Candidate(name) for name in candidate_names]
        ballots = []

        for row in csvfile:

            sorted_row = {Candidate(name): vote
                          for name, vote
                          in sorted(
                            row.items(), key=lambda item: item[1]
                          )
                         }
            ballots.append(Ballot(
                ranked_candidates=list(sorted_row.keys())
            ))

        return candidates, ballots


if __name__ == "__main__":
    subprocess.call(['rm', 'deduped_voting.csv'])
    _remove_duplicates()
    candidates, ballots = _raw_votes()
    election_result = single_transferable_vote(
        candidates, ballots, number_of_seats=2
    )
    print(election_result)
