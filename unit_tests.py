import unittest
from unittest.mock import patch
from io import StringIO
from solution import Solution, PolicyNameError, PolicyDocumentError, StatementError


class TestSolution(unittest.TestCase):

    def test_unexpected_keys_first_level(self):
        filename = "tests/unexpected_keys_first_level.json"
        with self.assertRaises(PolicyNameError) as context:
            solution = Solution(filename=filename)
            solution.validate_AWS_keys_first_and_second_level()
        self.assertEqual(
            str(context.exception),
            "Unexpected key(s) on first level: {'Unexpected_key'}"
        )
        solution.close_file()

    def test_unexpected_keys_second_level(self):
        filename = "tests/unexpected_keys_second_level.json"
        with self.assertRaises(PolicyDocumentError) as context:
            solution = Solution(filename=filename)
            solution.validate_AWS_keys_first_and_second_level()
        self.assertEqual(
            str(context.exception),
            "Unexpected key(s) on second level: {'Unexpected_key'}"
        )
        solution.close_file()

    def test_missing_policy_name(self):
        filename = "tests/missing_policy_name.json"
        with self.assertRaises(PolicyNameError) as context:
            solution = Solution(filename=filename)
            solution.validate_PolicyName()
        self.assertEqual(
            str(context.exception),
            "Missing required key 'PolicyName'!"
        )
        solution.close_file()

    def test_policy_name_length(self):
        filename = "tests/policy_name_length.json"
        with self.assertRaises(PolicyNameError) as context:
            solution = Solution(filename=filename)
            solution.validate_PolicyName()
        self.assertEqual(
            str(context.exception),
            "Length of value for required key 'PolicyName' has to be between 1 and 128!"
        )
        solution.close_file()

    def test_policy_name_pattern(self):
        filename = "tests/policy_name_pattern.json"
        with self.assertRaises(PolicyNameError) as context:
            solution = Solution(filename=filename)
            solution.validate_PolicyName()
        self.assertEqual(
            str(context.exception),
            "Value for required key 'PolicyName' does not match the [\\w+=,.@-]+ pattern!"
        )
        solution.close_file()

    def test_missing_policy_document(self):
        filename = "tests/missing_policy_document.json"
        with self.assertRaises(PolicyDocumentError) as context:
            solution = Solution(filename=filename)
            solution.validate_PolicyDocument()
        self.assertEqual(
            str(context.exception),
            "Missing required key 'PolicyDocument'!"
        )
        solution.close_file()

    def test_missing_version(self):
        filename = "tests/missing_version.json"
        with self.assertRaises(PolicyDocumentError) as context:
            solution = Solution(filename=filename)
            solution.validate_PolicyDocument()
        self.assertEqual(
            str(context.exception),
            "Missing key 'Version' in PolicyDocument!"
        )
        solution.close_file()

    def test_missing_statement(self):
        filename = "tests/missing_statement.json"
        with self.assertRaises(PolicyDocumentError) as context:
            solution = Solution(filename=filename)
            solution.validate_PolicyDocument()
        self.assertEqual(
            str(context.exception),
            "Missing key 'Statement' in PolicyDocument!"
        )
        solution.close_file()

    def test_missing_effect(self):
        filename = "tests/missing_effect.json"
        with self.assertRaises(StatementError) as context:
            solution = Solution(filename=filename)
            solution.run()
        self.assertEqual(
            str(context.exception),
            "Missing key 'Effect' in statement with index 0!"
        )

    def test_invalid_effect_value(self):
        filename = "tests/invalid_effect_value.json"
        with self.assertRaises(StatementError) as context:
            solution = Solution(filename=filename)
            solution.run()
        self.assertEqual(
            str(context.exception),
            "Invalid value 'Invalid_value' for key 'Effect' in statement with index 0! Value for 'Effect' has to be 'Allow' or 'Deny'."
        )

    def test_missing_action(self):
        filename = "tests/missing_action.json"
        with self.assertRaises(StatementError) as context:
            solution = Solution(filename=filename)
            solution.run()
        self.assertEqual(
            str(context.exception),
            "Missing key 'Action' in statement with index 0!"
        )

    def test_missing_resource(self):
        filename = "tests/missing_resource.json"
        with self.assertRaises(StatementError) as context:
            solution = Solution(filename=filename)
            solution.run()
        self.assertEqual(
            str(context.exception),
            "Missing key 'Resource' in statement with index 0!"
        )

    def test_unexpected_keys_in_statement(self):
        filename = "tests/unexpected_keys_statement.json"
        solution = Solution(filename=filename)
        with self.assertRaises(StatementError) as context:
            solution.run()
        self.assertIn("Unexpected key(s) {'Unexpected_key'} in statement with index 0!", str(
            context.exception))

    def test_resource_method_False(self):
        filename = "tests/valid_data.json"
        expected_output = "Method returned False for statement with index 0."
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            solution = Solution(filename=filename)
            solution.run()
            last_print_statement = mock_stdout.getvalue().strip().split(
                '\n')[-1]
        self.assertEqual(last_print_statement, expected_output)

    def test_resource_method_True(self):
        filename = "tests/valid_data_resource_true.json"
        expected_output = "Method returned True for statement with index 0."
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            solution = Solution(filename=filename)
            solution.run()
            last_print_statement = mock_stdout.getvalue().strip().split(
                '\n')[-1]
        self.assertEqual(last_print_statement, expected_output)


if __name__ == '__main__':
    unittest.main()
