## exceptions.py
## IS 601 Module 5
## Evan Garvey

## This file contains the exception hierarchy for the calculator

class CalculatorError(Exception):

    ## Base case for the exception hierarchy. More specific errors are seen below

    pass

class ValidationError(CalculatorError):

    ## Used when the input cannot be validated / is invalid

    pass

class OperationError(CalculatorError):

    ## Used when the operation fails

    pass

class ConfigurationError(CalculatorError):

    ## Used when the configuration is invalid

    pass