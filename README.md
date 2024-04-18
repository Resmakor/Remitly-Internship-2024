# Remitly Internship 2024
Project created as part of Remitly's 2024 internship recruitment. The project consisted of creating an application to verify JSON files in [AWS::IAM:Role Policy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-role-policy.html) format and writing a method to check if the value for the `Resource` field is an asterisk or some other value. Method shall return logical false if an input JSON Resource field contains a single asterisk and true in any other case.

# AWS::IAM:Role Policy JSON example
![AWS::IAM:Role Policy example](https://github.com/Resmakor/Remitly-Internship-2024/blob/main/iam_role_policy_properties/aws_iam_role_policy_example.PNG?raw=true)
#

# About PolicyName and PolicyDocument
![About PolicyName and PolicyDocument](https://github.com/Resmakor/Remitly-Internship-2024/blob/main/iam_role_policy_properties/PolicyName_and_PolicyDocument.PNG?raw=true)
#

# More about PolicyDocument
![More about PolicyDocument](https://github.com/Resmakor/Remitly-Internship-2024/blob/main/iam_role_policy_properties/PolicyDocument_terms.PNG?raw=true)
#


# Starting up
If you do not have the Python language installed, you can download it [here](https://www.python.org/downloads/).

If you do have it start the terminal in the ``Remitly-Internship-2024`` directory and type ``python main.py``. By default it should display: ``Method returned False for statement with index 0.``

To test the programme for different variants of the JSON structure (including error handling) you can modify the ``data.json`` file to your own expectations.

To run 15 tests for different cases start the terminal in the Remitly-Internship-2024 directory and type ``python unit_tests.py``. The name of each JSON file in the ``tests`` folder suggests what will be verified during the unit test.
#


# File `solution.py`

# Class ```PolicyNameError```
- Class created to make PolicyName errors easy to read and grouped together.

#

# Class ```PolicyDocumentError```
- Class created to make PolicyDocument errors easy to read and grouped together.

#

# Class ```StatementError```
- Class created to make Statement errors easy to read and grouped together.

#

# Class ```Solution```

## Members

```python
self.policy_name_pattern
```
- The regular expression that defines the PolicyName. The default value is ```[\w+=,.@-]+```
```python
self.warnings
```
- Flag on whether to display warnings or not. Set to ``False`` (do not display) by default. NOTE: If you change the flag to ``True`` in your code, unit tests will not work properly.
```python
self.filename
```
- JSON file name. By default, the file is called ``data.json`` and it is in the same folder as the ``solution.py`` file.
```python
self.file
```
- The variable that is responsible for accessing the file. When the object is created, it is initialised with whatever the ``self.open_file`` method returns.
```python
self.data_json
```
- The variable that is responsible for accessing the loaded JSON.
```python
sys.tracebacklimit = 0
```
- The command that makes error messages more readable (there will be no exact error information from the programmer's point of view).
#

## Methods

```python
def open_file(self, filename):
```
- The method opens a file with the specified filename and returns a file object, handling exceptions if the file cannot be opened.
#

```python
def close_file(self):
```
- The method closes the file that is currently open.
#

```python
def validate_json(self):
```
- The method attempts to load JSON data from the currently open file and returns the parsed JSON object, raising an exception if there are any errors during the process.
#

```python
def validate_AWS_keys_first_and_second_level(self):
```
- The method checks the keys within a JSON object (```data_json```) representing an AWS policy. It ensures that the first level keys includes "PolicyDocument" and "PolicyName", while the second level keys within "PolicyDocument" includes "Version" and "Statement". If any unexpected keys are found, it raises ``PolicyNameError`` or ``PolicyDocumentError`` with corresponding messages. I assumed there may be copies overwriting.
#

```python
def validate_regex(self, regex, text):
```
- The method validates whether a given regular expression pattern (``regex``) matches the provided text (``text``). It returns a boolean indicating whether there's a match found using the ``re.match()`` function.
#

```python
def validate_PolicyName(self):
```
- The method ensures that the "PolicyName" key exists in the JSON data (``data_json``) and meets certain criteria. It raises a ``PolicyNameError`` with appropriate messages if: 
1. "PolicyName" key is missing. 
2. Length of the "PolicyName" value is either too short (less than 1 character) or too long (more than 128 characters). 
3. The "PolicyName" value does not match the specified pattern (``policy_name_pattern``) using the ``validate_regex`` function.
#

```python
def validate_PolicyDocument(self):
```
- The method ensures that the JSON data (``data_json``) contains the required keys within the "PolicyDocument" object. It raises a ``PolicyDocumentError`` with appropriate messages if:
1. "PolicyDocument" key is missing.
2. "Version" or "Statement" keys are missing. 

If all required keys are present, it returns the ``PolicyDocument_json`` object for further processing.
#


```python
def validate_Statement(self, index, statement):
```
- The method validates an individual statement within an AWS policy. It checks if the statement contains all the required keys ("Effect", "Action", "Resource") and raises a ``StatementError`` with appropriate messages if any key is missing or if there are unexpected keys. Additionally, it checks for specific values for the "Effect" key ("Allow" or "Deny") and prints warnings if optional keys ("Sid", "Principal", "Condition") are not included, depending on the warnings flag.
#

```python
def validate_Resource(self, resource):
```
- The method validates the resource specified in the AWS policy. It returns ``False`` if the resource is set to '*', otherwise it returns ``True``. This is the method that was required in the task conditions.
# 

```python
def run(self):
```
- The method arranges the validation process for an AWS policy. It first validates the policy name, then validates the policy document structure and keys, iterates through each statement within the policy document to validate them individually using the ``validate_Statement`` function and prints the result of ``validate_Resource`` for each statement. Finally, it ensures the file is closed regardless of whether an exception occurs during the process.
# 

# File `main.py`
- In the ``main.py`` file, an instance of the ``Solution`` class is created with the warnings parameter set to ``False`` (default value) and the filename parameter set to "``data.json``". Then, the run method of the ``Solution`` instance is called to execute the validation process defined in the solution file.

# File `unit_tests.py`
- In the ``unit_tests.py``, various test cases are defined to validate the functionality of the ``Solution`` class methods. These tests cover scenarios such as unexpected keys at different levels, missing keys, invalid key values, and correct resource validation. Each test case creates an instance of ``Solution`` object with a specific test file, invokes the relevant method and asserts that the expected exceptions or output are raised or printed. 
For some tests, the ``unittest.mock.patch`` module is used to mock the standard output (``sys.stdout``) to capture printed statements, allowing for assertion of the printed output. Finally, the ``unittest.main()`` function is called to execute all the defined test cases when the script is run directly.

# Folder `tests`
- Folder with JSON files that are used for unit tests. The name of each file suggests what will be tested.

# Folder `iam_role_policy_properties`
- Folder with the images used in the README file.