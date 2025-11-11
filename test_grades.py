"""
Comprehensive unit tests for the grade processing functions.
Tests cover basic functionality, edge cases, validation, and error handling.
"""

import unittest
from chat_and_code_explain import (
    process_grades,
    process_grades_optimized,
    get_letter_grade,
    letter_to_numeric_grade,
    convert_to_numeric_grade,
    validate_grades_input,
    validate_individual_grade,
    calculate_grade_distribution,
    get_grade_summary
)


class TestGradeProcessing(unittest.TestCase):
    """Test suite for grade processing functions."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.valid_numeric_grades = [85, 92, 78, 96, 88, 73, 91, 87, 82, 94]
        self.valid_letter_grades = ['A', 'B+', 'B', 'C-', 'A-', 'D+', 'F', 'C', 'B-']
        self.mixed_grades = [95, 'B+', 78, 'A-', 85, 'C', 92, 'D+', 73, 'F']
        self.invalid_grades = [150, -10, 'X', None, '', 'invalid']

    def test_basic_numeric_grades(self):
        """Test basic functionality with valid numeric grades."""
        result = process_grades(self.valid_numeric_grades)
        
        # Check required fields exist
        self.assertIn('average', result)
        self.assertIn('highest', result)
        self.assertIn('lowest', result)
        self.assertIn('total_students', result)
        self.assertIn('grade_distribution', result)
        self.assertIn('validation_stats', result)
        
        # Check calculated values
        self.assertEqual(result['total_students'], 10)
        self.assertEqual(result['highest'], 96.0)
        self.assertEqual(result['lowest'], 73.0)
        self.assertAlmostEqual(result['average'], 86.6, places=1)
        
        # Check validation stats
        self.assertEqual(result['validation_stats']['valid_count'], 10)
        self.assertEqual(result['validation_stats']['invalid_count'], 0)
        self.assertEqual(result['validation_stats']['success_rate'], 100.0)

    def test_letter_grades(self):
        """Test functionality with letter grades."""
        result = process_grades(self.valid_letter_grades)
        
        self.assertIn('average', result)
        self.assertEqual(result['total_students'], 9)
        self.assertGreater(result['average'], 0)
        self.assertLessEqual(result['average'], 100)
        
        # Check grade distribution has all categories
        dist = result['grade_distribution']
        self.assertIn('A', dist)
        self.assertIn('B', dist)
        self.assertIn('C', dist)
        self.assertIn('D', dist)
        self.assertIn('F', dist)

    def test_mixed_grades(self):
        """Test functionality with mixed numeric and letter grades."""
        result = process_grades(self.mixed_grades)
        
        self.assertEqual(result['total_students'], 10)
        self.assertIn('validation_stats', result)
        self.assertEqual(result['validation_stats']['valid_count'], 10)
        self.assertEqual(result['validation_stats']['success_rate'], 100.0)

    def test_empty_list(self):
        """Test handling of empty grade list."""
        result = process_grades([])
        
        self.assertIn('error', result)
        self.assertEqual(result['error_code'], 'EMPTY_LIST')

    def test_none_input(self):
        """Test handling of None input."""
        result = process_grades(None)
        
        self.assertIn('error', result)
        self.assertEqual(result['error_code'], 'NULL_INPUT')

    def test_invalid_type_input(self):
        """Test handling of non-list input types."""
        test_cases = [
            "85,92,78",  # String
            85,          # Integer
            {'grades': [85, 92]},  # Dictionary
            (85, 92, 78)  # Tuple
        ]
        
        for invalid_input in test_cases:
            with self.subTest(input_type=type(invalid_input).__name__):
                result = process_grades(invalid_input)
                self.assertIn('error', result)
                self.assertEqual(result['error_code'], 'INVALID_TYPE')

    def test_size_validation(self):
        """Test size validation with custom limits."""
        # Test minimum students
        result = process_grades([85], min_students=3)
        self.assertIn('error', result)
        self.assertEqual(result['error_code'], 'TOO_FEW_STUDENTS')
        
        # Test maximum students
        large_list = [85] * 50
        result = process_grades(large_list, max_students=10)
        self.assertIn('error', result)
        self.assertEqual(result['error_code'], 'TOO_MANY_STUDENTS')

    def test_all_invalid_grades(self):
        """Test handling when all grades are invalid."""
        result = process_grades(self.invalid_grades)
        
        self.assertIn('error', result)
        self.assertEqual(result['error_code'], 'NO_VALID_GRADES')
        self.assertIn('invalid_details', result)
        self.assertEqual(result['invalid_count'], len(self.invalid_grades))

    def test_mixed_valid_invalid_grades(self):
        """Test handling of mixed valid and invalid grades."""
        mixed_invalid = [85, 'B+', None, '', 'X', 92, 'A']
        result = process_grades(mixed_invalid)
        
        # Should process valid grades
        self.assertIn('average', result)
        self.assertIn('warnings', result)
        
        # Check validation stats
        stats = result['validation_stats']
        self.assertEqual(stats['total_entries'], 7)
        self.assertGreater(stats['valid_count'], 0)
        self.assertGreater(stats['invalid_count'], 0)
        self.assertLess(stats['success_rate'], 100.0)

    def test_suspicious_data_patterns(self):
        """Test detection of suspicious data patterns."""
        # All identical values
        identical_data = [85] * 25
        result = process_grades(identical_data)
        self.assertIn('warning', result)
        
        # Mostly None values
        mostly_none = [85] + [None] * 10
        result = process_grades(mostly_none)
        self.assertIn('error', result)
        self.assertEqual(result['error_code'], 'CORRUPTED_DATA')

    def test_edge_case_grades(self):
        """Test edge case grade values."""
        edge_cases = [0, 100, 0.1, 99.9]
        result = process_grades(edge_cases)
        
        self.assertEqual(result['total_students'], 4)
        self.assertEqual(result['lowest'], 0.0)
        self.assertEqual(result['highest'], 100.0)

    def test_optimized_version_consistency(self):
        """Test that optimized version produces same results."""
        test_cases = [
            self.valid_numeric_grades,
            self.valid_letter_grades,
            self.mixed_grades
        ]
        
        for grades in test_cases:
            with self.subTest(grades=grades[:3]):  # Show first 3 for clarity
                result1 = process_grades(grades)
                result2 = process_grades_optimized(grades)
                
                # Compare key statistics (optimized version might not have all fields)
                if 'average' in result1 and 'average' in result2:
                    self.assertAlmostEqual(result1['average'], result2['average'], places=2)
                    self.assertEqual(result1['highest'], result2['highest'])
                    self.assertEqual(result1['lowest'], result2['lowest'])
                    self.assertEqual(result1['total_students'], result2['total_students'])


class TestHelperFunctions(unittest.TestCase):
    """Test suite for helper functions."""

    def test_get_letter_grade(self):
        """Test numeric to letter grade conversion."""
        test_cases = [
            (95, 'A'), (90, 'A'), (89, 'B'), (85, 'B'),
            (79, 'C'), (75, 'C'), (69, 'D'), (65, 'D'),
            (59, 'F'), (0, 'F')
        ]
        
        for numeric, expected_letter in test_cases:
            with self.subTest(grade=numeric):
                self.assertEqual(get_letter_grade(numeric), expected_letter)

    def test_letter_to_numeric_grade(self):
        """Test letter to numeric grade conversion."""
        test_cases = [
            ('A', 95.0), ('B', 85.0), ('C', 75.0), ('D', 65.0), ('F', 50.0),
            ('A+', 98.0), ('A-', 92.0), ('B+', 88.0), ('B-', 82.0),
            ('a', 95.0), ('b+', 88.0), ('C-', 72.0)  # Case variations
        ]
        
        for letter, expected_numeric in test_cases:
            with self.subTest(letter=letter):
                result = letter_to_numeric_grade(letter)
                self.assertAlmostEqual(result, expected_numeric, places=1)

    def test_letter_to_numeric_invalid(self):
        """Test letter grade conversion with invalid inputs."""
        invalid_letters = ['X', 'Z', 'G', '', None, 123]
        
        for invalid_letter in invalid_letters:
            with self.subTest(letter=invalid_letter):
                result = letter_to_numeric_grade(invalid_letter)
                self.assertIsNone(result)

    def test_convert_to_numeric_grade(self):
        """Test universal grade conversion function."""
        test_cases = [
            # Numeric grades
            (85, 85.0), (92.5, 92.5), ('78', 78.0), ('95.5', 95.5),
            # Letter grades
            ('A', 95.0), ('B+', 88.0), ('C-', 72.0),
            # Invalid grades
            (150, None), (-10, None), ('X', None), (None, None), ('', None)
        ]
        
        for input_grade, expected_output in test_cases:
            with self.subTest(input=input_grade):
                result = convert_to_numeric_grade(input_grade)
                if expected_output is None:
                    self.assertIsNone(result)
                else:
                    self.assertAlmostEqual(result, expected_output, places=1)

    def test_validate_individual_grade(self):
        """Test individual grade validation."""
        # Valid grades
        valid_cases = [85, 'A', 'B+', '92', 0, 100]
        for grade in valid_cases:
            with self.subTest(grade=grade):
                result = validate_individual_grade(grade)
                self.assertTrue(result['valid'])
                self.assertIn('numeric_value', result)
        
        # Invalid grades
        invalid_cases = [None, '', 'X', 150, -10]
        for grade in invalid_cases:
            with self.subTest(grade=grade):
                result = validate_individual_grade(grade)
                self.assertFalse(result['valid'])
                self.assertIn('error', result)
                self.assertIn('suggestion', result)

    def test_calculate_grade_distribution(self):
        """Test grade distribution calculation."""
        grades = [95, 85, 75, 65, 55]  # One of each letter grade
        distribution = calculate_grade_distribution(grades)
        
        # Check structure
        for letter in ['A', 'B', 'C', 'D', 'F']:
            self.assertIn(letter, distribution)
            self.assertIn('count', distribution[letter])
            self.assertIn('percentage', distribution[letter])
        
        # Check counts
        self.assertEqual(distribution['A']['count'], 1)
        self.assertEqual(distribution['B']['count'], 1)
        self.assertEqual(distribution['C']['count'], 1)
        self.assertEqual(distribution['D']['count'], 1)
        self.assertEqual(distribution['F']['count'], 1)
        
        # Check percentages
        for letter in distribution:
            self.assertEqual(distribution[letter]['percentage'], 20.0)

    def test_get_grade_summary(self):
        """Test grade summary generation."""
        # Create a test result
        test_result = {
            'average': 85.5,
            'total_students': 10,
            'grade_distribution': {
                'A': {'count': 3}, 'B': {'count': 3}, 'C': {'count': 2},
                'D': {'count': 1}, 'F': {'count': 1}
            }
        }
        
        summary = get_grade_summary(test_result)
        self.assertIn('Good', summary)  # Average 85.5 should be "Good"
        self.assertIn('90.0%', summary)  # Pass rate should be 90%


class TestErrorHandling(unittest.TestCase):
    """Test suite for error handling and edge cases."""

    def test_special_float_values(self):
        """Test handling of special float values."""
        special_values = [float('inf'), float('-inf'), float('nan')]
        grades_with_special = [85] + special_values
        
        result = process_grades(grades_with_special)
        
        # Should process the valid grade and skip special values
        self.assertEqual(result['total_students'], 1)
        self.assertIn('warnings', result)
        self.assertGreater(result['validation_stats']['invalid_count'], 0)

    def test_very_large_numbers(self):
        """Test handling of very large numeric values."""
        large_numbers = [1e20, -1e20, 85, 92]
        result = process_grades(large_numbers)
        
        # Should only process the valid grades (85, 92)
        self.assertEqual(result['total_students'], 2)
        self.assertIn('warnings', result)

    def test_string_numeric_edge_cases(self):
        """Test edge cases in string numeric conversion."""
        edge_cases = ['85.0', '92.99', '100.00', '0.1', '99.9']
        result = process_grades(edge_cases)
        
        self.assertEqual(result['total_students'], 5)
        self.assertEqual(result['validation_stats']['success_rate'], 100.0)

    def test_whitespace_handling(self):
        """Test handling of whitespace in grades."""
        whitespace_grades = [' 85 ', '\t92\t', '\n78\n', '  A  ', ' B+ ']
        result = process_grades(whitespace_grades)
        
        # Should handle whitespace gracefully
        self.assertGreater(result['total_students'], 0)

    def test_case_sensitivity(self):
        """Test case insensitive letter grade handling."""
        case_variations = ['a', 'B', 'c+', 'D-', 'f']
        result = process_grades(case_variations)
        
        self.assertEqual(result['total_students'], 5)
        self.assertEqual(result['validation_stats']['success_rate'], 100.0)


def run_performance_test():
    """Run performance comparison between standard and optimized versions."""
    import time
    
    # Generate test data
    large_dataset = [85, 92, 78, 96, 88] * 1000  # 5000 grades
    
    print("\n" + "="*50)
    print("PERFORMANCE TEST")
    print("="*50)
    
    # Test standard version
    start_time = time.time()
    for _ in range(10):
        result1 = process_grades(large_dataset)
    standard_time = time.time() - start_time
    
    # Test optimized version
    start_time = time.time()
    for _ in range(10):
        result2 = process_grades_optimized(large_dataset)
    optimized_time = time.time() - start_time
    
    print(f"Standard version:  {standard_time:.4f}s (10 iterations)")
    print(f"Optimized version: {optimized_time:.4f}s (10 iterations)")
    
    if optimized_time > 0:
        speedup = standard_time / optimized_time
        print(f"Speedup: {speedup:.2f}x")
    
    # Verify results match
    results_match = (
        result1['average'] == result2['average'] and
        result1['total_students'] == result2['total_students']
    )
    print(f"Results consistent: {results_match}")


if __name__ == '__main__':
    # Run unit tests
    print("Running comprehensive unit tests for grade processing functions...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run performance test
    run_performance_test()