# Author: Ethan Rodgers-Gates
# This is a CL script that accepts a raw ACT section score, form name, and specified section, and calculates
# the scaled score for that official form's score breakdown
from datetime import datetime
from typing import Dict

ENHANCED_CUTOFF = datetime(2025, 4)
    
class Form:
    """An official ACT form with identifier and test date"""
    def __init__(self, form_id: str, test_date: datetime):
        self.form_id = form_id
        self.test_date = test_date
        self.is_enhanced = True if datetime >= ENHANCED_CUTOFF else False
    
    def get_form_num(self) -> str:
        return self.form_id
    def get_test_date(self) -> datetime:
        return self.test_date

class ConversionTable:
    """Conversion table for four sections of an official ACT"""
    def __init__(self, mapping: Dict[str, Dict[tuple, int]]):
        """
        mapping: dict[str, dict[tuple, int]]
            Example: 
                {"english": 
                    {(74, 75): 36, (71, 73): 35, (69, 70): 34, ...}
                    ...
                }
        """
        self.mapping = mapping
    
    def convert(self, section: str, raw_score: int) -> int:
        """Accepts section type and raw section score and performs lookup in mapping to get scaled ACT score"""
        sect_low = section.lower()
        sect_mapping = self.mapping.get(sect_low)
        for raw, scale in sect_mapping.items(): 
            if raw[0] <= raw_score <= raw[1]: # key is in the form (raw_lower, raw_higher) as a range of possible raw scores
                return scale
        


form = Form("H11", datetime(2024, 9))
mapping = {"english": {(73, 75): 36, (71, 73): 35, (69, 70): 34},
           "math": {(59, 60): 36, (57, 58): 35, (56, 56): 34},
           "reading": {(38, 40): 36, (37, 37): 35, (35, 36): 34},
           "science": {(40, 40): 36, (39, 39): 35, (38, 38): 34}
           }









