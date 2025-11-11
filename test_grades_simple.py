"""
Simple test runner for the grade processing functions.
Run this to execute all unit tests without performance comparison.
"""

import unittest
from chat_and_code_explain import (
    process_grades,
    get_letter_grade,
    letter_to_numeric_grade,
    convert_to_numeric_grade,
    calculate_grade_distribution,
    get_grade_summary
)

class TestGradeProcessingBasic(unittest.TestCase):
    """Essential tests for grade processing functions."""

    def test_basic_functionality(self):
        """Test basic grade processing with numeric grades."""
        grades = [85, 92, 78, 96, 88, 73, 91, 87, 82, 94]
        result = process_grades(grades)
        
        # Check all required fields are present
        self.assertIn('average', result)
        self.assertIn('highest', result)
        self.assertIn('lowest', result)
        self.assertIn('total_students', result)
        self.assertIn('grade_distribution', result)
        
        # Verify calculations
        self.assertEqual(result['total_students'], 10)
        self.assertEqual(result['highest'], 96.0)
        self.assertEqual(result['lowest'], 73.0)
        self.assertAlmostEqual(result['average'], 86.6, places=1)

    def test_letter_grades(self):
        """Test letter grade processing."""
        grades = ['A', 'B+', 'C', 'D-', 'F']
        result = process_grades(grades)
        
        self.assertEqual(result['total_students'], 5)
        self.assertIn('grade_distribution', result)
        self.assertGreater(result['average'], 0)

    def test_mixed_grades(self):
        """Test mixed numeric and letter grades."""
        grades = [95, 'B+', 78, 'A-', 85]
        result = process_grades(grades)
        
        self.assertEqual(result['total_students'], 5)
        self.assertIn('validation_stats', result)

    def test_error_handling(self):
        """Test various error conditions."""
        # Empty list
        result = process_grades([])
        self.assertIn('error', result)
        
        # Invalid type
        result = process_grades("not a list")
        self.assertIn('error', result)
        
        # None input
        result = process_grades(None)
        self.assertIn('error', result)

    def test_invalid_grades(self):
        """Test handling of invalid grades."""
        grades = [85, 150, -10, 'X', None, '', 92]
        result = process_grades(grades)
        
        # Should process valid grades and warn about invalid ones
        self.assertGreater(result['total_students'], 0)
        self.assertIn('warnings', result)

    def test_helper_functions(self):
        """Test helper functions."""
        # Letter to numeric conversion
        self.assertEqual(letter_to_numeric_grade('A'), 95.0)
        self.assertEqual(letter_to_numeric_grade('B+'), 88.0)
        self.assertIsNone(letter_to_numeric_grade('X'))
        
        # Numeric to letter conversion
        self.assertEqual(get_letter_grade(95), 'A')
        self.assertEqual(get_letter_grade(85), 'B')
        self.assertEqual(get_letter_grade(75), 'C')
        
        # Universal conversion
        self.assertEqual(convert_to_numeric_grade(85), 85.0)
        self.assertEqual(convert_to_numeric_grade('A'), 95.0)
        self.assertIsNone(convert_to_numeric_grade('X'))

    def test_grade_distribution(self):
        """Test grade distribution calculation."""
        grades = [95, 85, 75, 65, 55]  # One of each letter
        distribution = calculate_grade_distribution(grades)
        
        for letter in ['A', 'B', 'C', 'D', 'F']:
            self.assertIn(letter, distribution)
            self.assertEqual(distribution[letter]['count'], 1)
            self.assertEqual(distribution[letter]['percentage'], 20.0)

    def test_validation_stats(self):
        """Test validation statistics."""
        valid_grades = [85, 92, 78]
        result = process_grades(valid_grades)
        
        stats = result['validation_stats']
        self.assertEqual(stats['total_entries'], 3)
        self.assertEqual(stats['valid_count'], 3)
        self.assertEqual(stats['invalid_count'], 0)
        self.assertEqual(stats['success_rate'], 100.0)

if __name__ == '__main__':
    print("🧪 Running Grade Processing Unit Tests")
    print("="*50)
    
    # Run the tests
    unittest.main(verbosity=2)