## calculation.py
## IS 601 Module 5
## Evan Garvey

## This file contains the Calculation class, which handles individual calculations

from dataclasses import dataclass, field
import datetime
from decimal import Decimal, InvalidOperation
import logging
from typing import Any, Dict
from app.exceptions import OperationError

## The Calculation dataclass will handle some of the logic the user sends to and recieves from the calculator. Operation calculations only

@dataclass
class Calculation:
    
    operation: str
    num1: Decimal
    num2: Decimal
    result: Decimal = field(init=False)
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __post_init__(self):
        
        self.result = self.calculate()

    def calculate(self) -> Decimal:

        operations = {
            "add": lambda x, y: x + y,
            "subtract": lambda x, y: x - y,
            "multiply": lambda x, y: x * y,
            "divide": lambda x, y: x / y if y != 0 else self._divide_by_zero_error(),       
            "power": lambda x, y: Decimal(pow(float(x), float(y))) 
            if y >= 0 else self._negative_exponent_error(),
            "root": lambda x,y: Decimal(pow(float(x), 1 / float(y)))
            if x >= 0 and y != 0 else self._negative_root_error()                                           
        }

        op = operations.get(self.operation)

        if not op:

            raise OperationError(f"Invalid operation: {self.operation}")
        
        try:

            return op(self.num1, self.num2)
        
        except (InvalidOperation, ValueError, ArithmeticError) as exc:

            raise OperationError(f"Calculation failed: {str(exc)}")
        

    @staticmethod
    def _divide_by_zero_error() -> OperationError:
        return OperationError("Cannot divide by zero")
    
    @staticmethod
    def _negative_exponent_error() -> OperationError:
        return OperationError("Cannot calculate negative exponents")
    
    @staticmethod
    def _negative_root_error() -> OperationError:
        return OperationError("Cannot calculate negative roots")
    
    def serialize(self) -> Dict[str, Any]:

        return {
            "operation": self.operation,
            "num1": str(self.num1),
            "num2": str(self.num2),
            "result": str(self.result),
            "timestamp": self.timestamp.isoformat()
        }
    
    @staticmethod
    def retrieve_calculation(data: Dict[str, Any]) -> "Calculation":

        try:

            calc = Calculation(
                operation=data["operation"],
                num1=Decimal(data["num1"]),
                num2=Decimal(data["num2"])
            )

            calc.timestamp = datetime.datetime.fromisoformat(data["timestamp"])

            temp_result = Decimal(data["result"])
            if temp_result != calc.result:
                
                logging.warning(f"Local result ({temp_result}) does not match stored result ({calc.result})")

            return calc

            return calc
        except(KeyError, InvalidOperation, ValueError) as exc:

            raise OperationError(f"Calculation data invalid: {str(exc)}")
        
    def __str__(self) -> str:

        return f"{self.num1} {self.operation} {self.num2} = {self.result}"
    
    def __repr__(self) -> str:

        return f"Calculation(operation={self.operation}, num1={self.num1}, num2={self.num2}, result={self.result}, timestamp={self.timestamp})"
    
    def __eq__(self, other: object) -> bool:

        if not isinstance(other, Calculation):

            return False
        
        return self.operation == other.operation and self.num1 == other.num1 and self.num2 == other.num2 and self.result == other.result
    
    def format_result(self, precision: int = 10) -> str:

        try:

            return str(self.result.normalize.quantize(Decimal("0." + "0" * precision)).normalize())
        
        except InvalidOperation as exc:

            return str(self.result)