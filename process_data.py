import sys
import json
import click
import pandas as pd

from modules.data_cleanup import DataCleanup
from modules.data_validation import DataValidation


class DataSanitization:
    def __init__(self, data_source):
        self.read_data(data_source)

    def read_data(self, data_source):
        self.df = pd.read_csv(data_source)
        self.df.rename(columns=lambda x: x.strip(), inplace=True)

    def write_data(self, output_file):
        self.df.to_csv(output_file, index=False)

    def cleanup(self, cleanup_rules):
        data_cleanup = DataCleanup(cleanup_rules)
        self.df = data_cleanup.cleanup(self.df)

    def validation(self, validation_rules):
        data_validation = DataValidation(validation_rules)
        data_validation.validate(self.df)
        self.validation_report = data_validation.validation_report()

    def get_validation_report(self):
        return self.validation_report

    def validation_report_in_json(self, report):
        return json.dumps(report, indent=4, sort_keys=True)


if __name__ == "__main__":

    # dirty_data_file = "data/data-dirty.csv"
    dirty_data_file = click.prompt(
        "Please enter dirty data file. default is: ", default="data/data-dirty.csv"
    )
    clean_data_file = "data/data-clean.csv"

    data_cleanup_rules_file = "data_rules/data_cleanup_rules.json"
    data_validation_rules_file = "data_rules/data_validation_rules.json"

    with open(data_cleanup_rules_file) as json_file:
        data_cleanup_rules = json.load(json_file)

    with open(data_validation_rules_file) as json_file:
        data_validation_rules = json.load(json_file)

    # Step 1. Do Pre Cleanup Validation
    data = DataSanitization(data_source=dirty_data_file)
    data.validation(data_validation_rules)
    pre_cleanup_data_report = data.get_validation_report()

    # Step 2. Do Data Cleanup
    data = DataSanitization(data_source=dirty_data_file)
    data.cleanup(data_cleanup_rules)

    # Step 3. Do Post Cleanup Validation
    data.validation(data_validation_rules)
    post_cleanup_data_report = data.get_validation_report()

    # Step 4. Write cleanup data to file
    data.write_data(clean_data_file)

    # Step 5. Display output to terminal

    # Display input/output files
    print("-" * 80)
    print("Input/Output files")
    print("-" * 80)
    print("Dirty data file:".ljust(35), dirty_data_file)
    print("Clean data output file:".ljust(35), clean_data_file)
    print("Cleanup rules file:".ljust(35), data_cleanup_rules_file)
    print("Validation rules file:".ljust(35), data_validation_rules_file)
    print("-" * 80)
    print('\n' * 1)

    # Disply Pre Cleanup Validation Check
    print("-" * 80)
    print("Pre data cleanup validation report [JSON format]")
    print("-" * 80)
    print(data.validation_report_in_json(pre_cleanup_data_report))

    print('\n' * 2)
    # Disply Pre Cleanup Validation Check
    print("-" * 80)
    print("Post data cleanup validation report [JSON format]")
    print("-" * 80)
    print(data.validation_report_in_json(post_cleanup_data_report))

    if len(post_cleanup_data_report["fail"]):
        print("Data file has issues. Process ends with status code (1)")
        sys.exit(1)

    print('\n'*2)
    print(f"*** Clean data file path is: {clean_data_file}")
    sys.exit(0)
