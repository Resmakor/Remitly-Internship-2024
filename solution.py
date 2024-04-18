import sys
import re
import json


class PolicyNameError(Exception):
    pass


class PolicyDocumentError(Exception):
    pass


class StatementError(Exception):
    pass


class Solution:
    def __init__(self, policy_name_pattern=r"[\w+=,.@-]+", warnings=False, filename="data.json"):
        self.policy_name_pattern = policy_name_pattern
        self.warnings = warnings
        self.filename = filename
        self.file = self.open_file(filename)
        self.data_json = self.validate_json()
        sys.tracebacklimit = 0

    def open_file(self, filename):
        try:
            file = open(filename)
        except Exception as e:
            raise Exception(f"{e}")
        return file

    def close_file(self):
        self.file.close()

    def validate_json(self):
        try:
            data_json = json.load(self.file)
        except Exception as e:
            raise Exception(f"{e}")
        return data_json

    def validate_AWS_keys_first_and_second_level(self):
        '''I assume there may be copies overwriting'''
        first_level_keys = self.data_json.keys()
        allowed_first_level_keys = {"PolicyDocument", "PolicyName"}
        if first_level_keys != allowed_first_level_keys:
            unexpected_first_level_keys = first_level_keys - allowed_first_level_keys
            raise PolicyNameError(
                f"Unexpected key(s) on first level: {unexpected_first_level_keys}")
        second_level_keys = set(self.data_json["PolicyDocument"].keys())
        allowed_second_level_keys = {"Version", "Statement"}
        if second_level_keys != allowed_second_level_keys:
            unexpected_second_level_keys = second_level_keys - allowed_second_level_keys
            raise PolicyDocumentError(
                f"Unexpected key(s) on second level: {unexpected_second_level_keys}")

    def validate_regex(self, regex, text):
        return bool(re.match(f"{regex}", text))

    def validate_PolicyName(self):
        if not "PolicyName" in self.data_json:
            raise PolicyNameError('Missing required key \'PolicyName\'!')
        if len(self.data_json["PolicyName"]) == 0 or len(self.data_json["PolicyName"]) > 128:
            raise PolicyNameError(
                "Length of value for required key \'PolicyName\' has to be between 1 and 128!")
        if not self.validate_regex(regex=self.policy_name_pattern, text=self.data_json["PolicyName"]):
            raise PolicyNameError(
                f'Value for required key \'PolicyName\' does not match the {self.policy_name_pattern} pattern!')

    def validate_PolicyDocument(self):
        if not "PolicyDocument" in self.data_json:
            raise PolicyDocumentError(
                'Missing required key \'PolicyDocument\'!')
        PolicyDocument_json = self.data_json['PolicyDocument']
        if not "Version" in PolicyDocument_json:
            raise PolicyDocumentError(
                'Missing key \'Version\' in PolicyDocument!')
        if not "Statement" in PolicyDocument_json:
            raise PolicyDocumentError(
                'Missing key \'Statement\' in PolicyDocument!')
        return PolicyDocument_json

    def validate_statement(self, index, statement):
        allowed_keys = {"Sid", "Effect", "Principal",
                        "Action", "Resource", "Condition"}
        unexpected_keys = set(statement.keys()) - allowed_keys
        if unexpected_keys:
            raise StatementError(
                f"Unexpected key(s) {unexpected_keys} in statement with index {index}!")
        if not "Sid" in statement and self.warnings:
            print(
                f'Warning: You may include key \'Sid\' in statement with index {index}!')
        if not "Effect" in statement:
            raise StatementError(
                f'Missing key \'Effect\' in statement with index {index}!')
        if statement['Effect'] != 'Allow' and statement['Effect'] != 'Deny':
            raise StatementError(
                f"Invalid value '{statement['Effect']}' for key 'Effect' in statement with index {index}! Value for 'Effect' has to be 'Allow' or 'Deny'.")
        if not "Principal" in statement and self.warnings:
            print(
                f'Warning: You may include key \'Principal\' in statement with index {index}!')
        if not "Action" in statement:
            raise StatementError(
                f'Missing key \'Action\' in statement with index {index}!')
        if not "Resource" in statement:
            raise StatementError(
                f'Missing key \'Resource\' in statement with index {index}!')
        if not "Condition" in statement and self.warnings:
            print(
                f'Warning: You may include key \'Condition\' in statement with index {index}!')

    def validate_resource(self, resource):
        if resource == '*':
            return False
        return True

    def run(self):
        try:
            self.validate_PolicyName()
            PolicyDocument_json = self.validate_PolicyDocument()
            self.validate_AWS_keys_first_and_second_level()
            PolicyDocuments_statements = PolicyDocument_json['Statement']
            for index, statement in enumerate(PolicyDocuments_statements):
                self.validate_statement(index, statement)
                print(
                    f"Method returned {self.validate_resource(statement['Resource'])} for statement with index {index}.")
        finally:
            self.close_file()
