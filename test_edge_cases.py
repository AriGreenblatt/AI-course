"""
Edge Case Test Suite for Grade Processing Functions
Tests the most critical edge cases that could break the system.
"""

import unittest
import sys
from chat_and_code_explain import process_grades, convert_to_numeric_grade

class TestCriticalEdgeCases(unittest.TestCase):
    """Critical edge cases that must be handled properly."""

    def test_boundary_values(self):
        """Test exact boundary values and near-boundary values."""
        # Exact boundaries
        exact_boundaries = [0, 0.0, 100, 100.0]
        result = process_grades(exact_boundaries)
        self.assertEqual(result['total_students'], 4)
        self.assertEqual(result['lowest'], 0.0)
        self.assertEqual(result['highest'], 100.0)
        
        # Just outside boundaries (should be rejected)
        outside_boundaries = [-0.1, 100.1, -1, 101]
        result = process_grades(outside_boundaries)
        self.assertIn('error', result)

    def test_special_float_values(self):
        """Test special float values that could cause crashes."""
        special_values = [float('inf'), float('-inf'), float('nan'), 85]
        result = process_grades(special_values)
        
        # Should only process the valid grade (85)
        self.assertEqual(result['total_students'], 1)
        self.assertIn('warnings', result)

    def test_empty_and_none_variations(self):
        """Test various empty/None scenarios."""
        test_cases = [
            ([None], "single None"),
            ([None, None], "multiple Nones"),
            ([""], "empty string"),
            ([None, ""], "mixed None and empty"),
            ([None, "", 85], "mixed with valid grade")
        ]
        
        for test_input, description in test_cases:
            with self.subTest(case=description):
                result = process_grades(test_input)
                if description == "mixed with valid grade":
                    self.assertEqual(result['total_students'], 1)
                    self.assertIn('warnings', result)
                else:
                    self.assertIn('error', result)

    def test_precision_edge_cases(self):
        """Test floating point precision edge cases."""
        precision_cases = [
            33.333333333333,  # Repeating decimal
            99.99999999999,   # Almost 100
            0.000000000001,   # Almost 0
            85.0000000001     # Tiny fraction
        ]
        
        result = process_grades(precision_cases)
        self.assertEqual(result['total_students'], 4)
        # Check that calculations don't break
        self.assertIsInstance(result['average'], float)

    def test_letter_grade_edge_cases(self):
        """Test edge cases in letter grade processing."""
        # Case and whitespace variations
        variations = ['a', 'A', ' B+ ', '\tC\t', 'D-', 'f ']
        result = process_grades(variations)
        self.assertGreater(result['total_students'], 0)
        
        # Invalid letter grades
        invalid_letters = ['X', 'Z', 'AA', 'A++', 'G']
        result = process_grades(invalid_letters)
        # Should reject all invalid letters
        self.assertIn('error', result)

    def test_mixed_data_chaos(self):
        """Test completely chaotic mixed data."""
        chaos_data = [
            85,              # Valid int
            'B+',            # Valid letter  
            None,            # None
            "",              # Empty string
            "invalid",       # Invalid string
            True,            # Boolean
            float('nan'),    # NaN
            [85],            # Nested list
        ]
        
        result = process_grades(chaos_data)
        # Should process the 2 valid grades and warn about others
        self.assertEqual(result['total_students'], 2)
        self.assertIn('warnings', result)

    def test_size_extremes(self):
        """Test size-related edge cases."""
        # Single grade
        single = [85]
        result = process_grades(single)
        self.assertEqual(result['total_students'], 1)
        
        # Large dataset (but within limits)
        large = [85, 92, 78] * 100  # 300 grades
        result = process_grades(large)
        self.assertEqual(result['total_students'], 300)
        
        # Too large dataset
        huge = [85] * 2000
        result = process_grades(huge, max_students=1000)
        self.assertIn('error', result)
        self.assertEqual(result['error_code'], 'TOO_MANY_STUDENTS')

    def test_statistical_edge_cases(self):
        """Test statistical calculation edge cases."""
        # All identical grades
        identical = [85] * 25
        result = process_grades(identical)
        self.assertEqual(result['average'], 85.0)
        self.assertEqual(result['highest'], 85.0)
        self.assertEqual(result['lowest'], 85.0)
        # Should trigger suspicious data warning
        self.assertIn('warning', result)
        
        # Extreme distributions
        all_perfect = [100] * 10
        result = process_grades(all_perfect)
        self.assertEqual(result['average'], 100.0)
        
        all_failing = [0] * 10  
        result = process_grades(all_failing)
        self.assertEqual(result['average'], 0.0)

    def test_string_numeric_edge_cases(self):
        """Test edge cases in string to numeric conversion."""
        string_numbers = [
            "85",           # Simple string number
            "85.0",         # String with decimal
            "085",          # Leading zero
            "85.00",        # Trailing zeros
            " 85 ",         # With spaces
            "8.5e1",        # Scientific notation (might not work)
        ]
        
        # Test each conversion individually
        for str_num in string_numbers:
            numeric = convert_to_numeric_grade(str_num)
            if numeric is not None:
                self.assertGreaterEqual(numeric, 0)
                self.assertLessEqual(numeric, 100)

    def test_unicode_and_encoding(self):
        """Test unicode and encoding edge cases."""
        unicode_cases = [
            'Á',             # Accented A (should be invalid)
            '８５',          # Full-width numbers (should be invalid)
            'А',             # Cyrillic A (looks like A but isn't)
        ]
        
        # These should all be invalid
        for unicode_char in unicode_cases:
            numeric = convert_to_numeric_grade(unicode_char)
            self.assertIsNone(numeric, f"Unicode '{unicode_char}' should be invalid")

    def test_memory_safety(self):
        """Test for potential memory issues."""
        # Very long string that looks like a number
        long_string = "85" + "0" * 1000
        result = convert_to_numeric_grade(long_string)
        # Should either convert or reject gracefully, not crash
        self.assertTrue(result is None or isinstance(result, (int, float)))
        
        # List with many invalid entries
        many_invalid = [None] * 1000 + [85]  # 1000 None + 1 valid
        result = process_grades(many_invalid, max_students=2000)
        self.assertEqual(result['total_students'], 1)


class TestSystemLimits(unittest.TestCase):
    """Test system and resource limits."""
    
    def test_recursion_safety(self):
        """Test that deeply nested or recursive structures don't crash."""
        # This shouldn't cause infinite recursion
        weird_input = [85, [92], [[78]], [[[96]]]]
        result = process_grades(weird_input)
        # Should handle gracefully (probably process 85 and reject the rest)
        self.assertIsInstance(result, dict)

    def test_memory_limits(self):
        """Test reasonable memory usage with large inputs."""
        # Test with reasonably large data
        large_data = list(range(85, 95)) * 100  # 1000 grades
        result = process_grades(large_data, max_students=2000)
        
        self.assertEqual(result['total_students'], 1000)
        # Should not consume excessive memory
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    print("🚨 Running Critical Edge Case Tests")
    print("="*50)
    
    # Run the edge case tests
    unittest.main(verbosity=2)