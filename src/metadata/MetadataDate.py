from datetime import datetime, date
from typing import Union
from dateutil import parser
from sampling_workflow.constraint.BoolConstraint import BoolConstraint
from sampling_workflow.metadata.Metadata import Metadata


class MetadataDate(Metadata[Union[datetime, date]]):
    
    def __init__(self, name: str):
        super().__init__(name, Union[datetime, date])

    def create_metadata_value(self, value):
        if not isinstance(value, self.type):
            try:
                typed_value=parser.parse(str(value)) 
            except Exception as e:
                raise TypeError(f"Value {value} date is not parsable" ) from e
        from sampling_workflow.metadata.MetadataValue import MetadataValue

        return MetadataValue(self, typed_value)


    def is_equal(self, value: Union[datetime, date]) -> BoolConstraint:
        return BoolConstraint(None, lambda x: x == value, self)

    def is_not_equal(self, value: Union[datetime, date]) -> BoolConstraint:
        return BoolConstraint(None, lambda x: x != value, self)

    def is_before(self, value: Union[datetime, date]) -> BoolConstraint:
        return BoolConstraint(None, lambda x: x < value, self)

    def is_after(self, value: Union[datetime, date]) -> BoolConstraint:
        return BoolConstraint(None, lambda x: x > value, self)

    def is_before_or_equal(self, value: Union[datetime, date]) -> BoolConstraint:
        return BoolConstraint(None, lambda x: x <= value, self)

    def is_after_or_equal(self, value: Union[datetime, date]) -> BoolConstraint:
        return BoolConstraint(None, lambda x: x >= value, self)

    def is_between(self, start: Union[datetime, date], end: Union[datetime, date]) -> BoolConstraint:
        return BoolConstraint(None, lambda x: start <= x <= end, self)

    def is_in_year(self, year: int) -> BoolConstraint:
        return BoolConstraint(None, lambda x: x.year == year, self)

    def is_in_month(self, month: int) -> BoolConstraint:
        return BoolConstraint(None, lambda x: x.month == month, self)

    def is_in_day(self, day: int) -> BoolConstraint:
        return BoolConstraint(None, lambda x: x.day == day, self)

    def is_weekday(self) -> BoolConstraint:
        """Check if the date is a weekday (Monday=0 to Friday=4)"""
        return BoolConstraint(None, lambda x: x.weekday() < 5, self)

    def is_weekend(self) -> BoolConstraint:
        """Check if the date is a weekend (Saturday=5 or Sunday=6)"""
        return BoolConstraint(None, lambda x: x.weekday() >= 5, self)
