"""
Copilot Chat and Code Explanation
Learning Objective
Learn to use Copilot Chat for code explanations, debugging, and optimization suggestions.

Instructions
Create a new Python file called data_processor.py
Write the initial code provided below
Use Copilot Chat to understand, improve, and extend the code
Practice asking specific questions about the code
Your Task
Start with this code that processes a list of student grades:

Copilot Chat Exercises
1. Code Explanation
Ask Copilot Chat:

"Explain what this process_grades function does"
"What is the purpose of the grade validation check?"
"Why do we check if count > 0 before calculating average?"
2. Code Improvement
Ask Copilot Chat:

"How can I make this code more readable?"
"Are there any potential bugs in this code?"
"How can I optimize this function?"
3. Feature Extension
Ask Copilot Chat:

"How can I add grade distribution (A, B, C, D, F) to this function?"
"How would I modify this to handle letter grades?"
"Can you help me add input validation?"
4. Testing
Ask Copilot Chat:

"Generate unit tests for this function"
"What edge cases should I test?"
"Create test data that would break this function"
What You'll Learn
How to effectively communicate with Copilot Chat
Using Chat for code review and improvement suggestions
Getting explanations for complex code logic
Generating test cases and documentation
Success Criteria
 You understand what the original code does
 You've implemented at least one improvement suggested by Chat
 You've added new features with Chat's help
 You have test cases for your function
Advanced Challenge
Ask Copilot Chat to help you:

Convert the function to use classes instead of dictionaries
Add logging to track function usage
Create a command-line interface for the grade processor
Questions to Explore
Try asking these questions in Copilot Chat:

"What are the time and space complexity of this function?"
"How would this code perform with 10,000 grades?"
"What would happen if someone passes a list with non-numeric values?"
"""

def validate_grades_input(grades, max_students=1000, min_students=1):
    """
    Comprehensive input validation for grades.
    
    Args:
        grades: Input to validate
        max_students (int): Maximum allowed number of students
        min_students (int): Minimum required number of students
        
    Returns:
        dict with error message if validation fails, None if valid
    """
    # 1. Check if input exists
    if grades is None:
        return {'error': 'Input cannot be None', 'error_code': 'NULL_INPUT'}
    
    # 2. Check if input is a list
    if not isinstance(grades, list):
        input_type = type(grades).__name__
        return {
            'error': f'Input must be a list, got {input_type}', 
            'error_code': 'INVALID_TYPE',
            'received_type': input_type
        }
    
    # 3. Check if list is empty
    if len(grades) == 0:
        return {'error': 'Grade list cannot be empty', 'error_code': 'EMPTY_LIST'}
    
    # 4. Check minimum students requirement
    if len(grades) < min_students:
        return {
            'error': f'At least {min_students} student(s) required, got {len(grades)}',
            'error_code': 'TOO_FEW_STUDENTS',
            'required': min_students,
            'received': len(grades)
        }
    
    # 5. Check maximum students limit (prevent memory issues)
    if len(grades) > max_students:
        return {
            'error': f'Too many students (max {max_students} allowed), got {len(grades)}',
            'error_code': 'TOO_MANY_STUDENTS',
            'limit': max_students,
            'received': len(grades)
        }
    
    # 6. Check for suspicious data patterns
    suspicious_check = check_suspicious_data(grades)
    if suspicious_check:
        return suspicious_check
    
    return None  # All validations passed


def check_suspicious_data(grades):
    """
    Check for suspicious data patterns that might indicate errors.
    
    Args:
        grades (list): List of grades to check
        
    Returns:
        dict with warning/error if suspicious patterns found, None if okay
    """
    # Count different data types
    none_count = sum(1 for g in grades if g is None)
    empty_string_count = sum(1 for g in grades if g == "")
    
    # 1. Too many None values (might indicate data corruption)
    if none_count > len(grades) * 0.5:  # More than 50% None
        return {
            'error': f'Too many missing values ({none_count}/{len(grades)}). Data might be corrupted.',
            'error_code': 'CORRUPTED_DATA',
            'none_count': none_count,
            'total_count': len(grades)
        }
    
    # 2. Too many empty strings
    if empty_string_count > len(grades) * 0.3:  # More than 30% empty
        return {
            'error': f'Too many empty grade entries ({empty_string_count}/{len(grades)})',
            'error_code': 'EMPTY_ENTRIES',
            'empty_count': empty_string_count
        }
    
    # 3. Check for extremely long lists of identical values (might be test data)
    if len(set(str(g) for g in grades if g is not None)) == 1 and len(grades) > 20:
        return {
            'warning': f'All {len(grades)} grades are identical. Is this test data?',
            'error_code': 'IDENTICAL_VALUES',
            'value': grades[0] if grades else None
        }
    
    return None


def validate_individual_grade(grade, position=None):
    """
    Validate a single grade entry and provide detailed feedback.
    
    Args:
        grade: Individual grade to validate
        position (int): Position in list for error reporting
        
    Returns:
        dict with validation info
    """
    pos_text = f" at position {position}" if position is not None else ""
    
    # Check for None
    if grade is None:
        return {
            'valid': False,
            'error': f'Missing grade{pos_text}',
            'suggestion': 'Remove or replace with valid grade'
        }
    
    # Check for empty string
    if grade == "":
        return {
            'valid': False,
            'error': f'Empty grade{pos_text}',
            'suggestion': 'Provide a numeric or letter grade'
        }
    
    # Try to convert to numeric
    numeric_grade = convert_to_numeric_grade(grade)
    if numeric_grade is not None:
        return {
            'valid': True,
            'numeric_value': numeric_grade,
            'original_value': grade
        }
    
    # If conversion failed, provide helpful suggestion
    grade_str = str(grade)
    if any(char in grade_str.upper() for char in 'ABCDF'):
        suggestion = "Check letter grade format (A, B, C, D, F with optional +/- )"
    elif any(char.isdigit() for char in grade_str):
        suggestion = "Numeric grades must be between 0-100"
    else:
        suggestion = "Use numeric grades (0-100) or letter grades (A-F)"
    
    return {
        'valid': False,
        'error': f'Invalid grade "{grade}"{pos_text}',
        'suggestion': suggestion
    }


def process_grades(grades, max_students=1000, min_students=1):
    """
    Analyze a list of student grades and return statistics with comprehensive validation.
    Supports both numeric grades (0-100) and letter grades (A, B, C, D, F).
    
    Args:
        grades (list): List of grades (numeric 0-100 or letters A-F with +/- modifiers)
        max_students (int): Maximum number of students allowed (default: 1000)
        min_students (int): Minimum number of students required (default: 1)
        
    Returns:
        dict: Contains average, highest, lowest grades and student count
        dict with 'error': Detailed error message if validation fails
    """
    # Comprehensive input validation
    validation_result = validate_grades_input(grades, max_students, min_students)
    if validation_result is not None:
        return validation_result
    
    # Initialize variables for calculations
    total_points = 0
    valid_grades_count = 0
    highest_grade = None  # Will be set to first valid grade
    lowest_grade = None   # Will be set to first valid grade
    
    # Enhanced validation and collection with detailed feedback
    valid_grades = []
    invalid_grades = []
    
    for i, grade in enumerate(grades):
        grade_validation = validate_individual_grade(grade, i)
        
        if grade_validation['valid']:
            valid_grades.append(grade_validation['numeric_value'])
        else:
            invalid_grades.append({
                'position': i,
                'value': grade,
                'error': grade_validation['error'],
                'suggestion': grade_validation['suggestion']
            })
    
    # Provide detailed error report if no valid grades
    if not valid_grades:
        error_details = {
            'error': 'No valid grades found',
            'error_code': 'NO_VALID_GRADES',
            'total_entries': len(grades),
            'invalid_count': len(invalid_grades),
            'invalid_details': invalid_grades[:5]  # Show first 5 invalid entries
        }
        
        if len(invalid_grades) > 5:
            error_details['additional_errors'] = len(invalid_grades) - 5
        
        return error_details
    
    # OPTIMIZATION: Use built-in functions (much faster than manual loops)
    total_points = sum(valid_grades)
    valid_grades_count = len(valid_grades)
    highest_grade = max(valid_grades)
    lowest_grade = min(valid_grades)
    
    # Calculate validation statistics
    validation_stats = {
        'total_entries': len(grades),
        'valid_count': len(valid_grades),
        'invalid_count': len(invalid_grades),
        'success_rate': round((len(valid_grades) / len(grades)) * 100, 1)
    }
    
    # Calculate average
    average_grade = total_points / valid_grades_count
    
    # Calculate grade distribution (A, B, C, D, F)
    grade_distribution = calculate_grade_distribution(valid_grades)
    
    result = {
        'average': round(average_grade, 2),
        'highest': highest_grade,
        'lowest': lowest_grade,
        'total_students': valid_grades_count,
        'grade_distribution': grade_distribution,
        'validation_stats': validation_stats
    }
    
    # Add warnings for invalid grades if any
    if invalid_grades:
        result['warnings'] = {
            'message': f'{len(invalid_grades)} invalid grade(s) were skipped',
            'invalid_entries': invalid_grades[:3]  # Show first 3 for reference
        }
        
        if len(invalid_grades) > 3:
            result['warnings']['additional_invalid'] = len(invalid_grades) - 3
    
    return result


def get_numeric_grade(grade):
    """
    Convert grade to numeric value if valid, otherwise return None.
    
    Args:
        grade: The grade value to convert and validate
        
    Returns:
        float: Numeric grade if valid (0-100), None otherwise
    """
    try:
        # Convert to float (handles int, float, and numeric strings)
        numeric_grade = float(grade)
        
        # Check if within valid range
        if 0 <= numeric_grade <= 100:
            return numeric_grade
        else:
            return None
    except (TypeError, ValueError):
        # Not a valid number
        return None


def get_letter_grade(numeric_grade):
    """
    Convert a numeric grade to a letter grade.
    
    Args:
        numeric_grade (float): Numeric grade (0-100)
        
    Returns:
        str: Letter grade (A, B, C, D, F)
    """
    if numeric_grade >= 90:
        return 'A'
    elif numeric_grade >= 80:
        return 'B'
    elif numeric_grade >= 70:
        return 'C'
    elif numeric_grade >= 60:
        return 'D'
    else:
        return 'F'


def letter_to_numeric_grade(letter_grade):
    """
    Convert a letter grade to a numeric grade using midpoint values.
    
    Args:
        letter_grade (str): Letter grade (A, B, C, D, F)
        
    Returns:
        float: Numeric equivalent or None if invalid
    """
    # Handle different letter grade formats
    if isinstance(letter_grade, str):
        letter = letter_grade.upper().strip()
        
        # Handle plus/minus grades
        base_grade = letter[0] if letter else ''
        modifier = letter[1:] if len(letter) > 1 else ''
        
        # Base grade values (using midpoint of each range)
        grade_map = {
            'A': 95.0,  # 90-100, midpoint = 95
            'B': 85.0,  # 80-89, midpoint = 85
            'C': 75.0,  # 70-79, midpoint = 75
            'D': 65.0,  # 60-69, midpoint = 65
            'F': 50.0   # 0-59, midpoint = 30 (but using 50 for calculations)
        }
        
        if base_grade in grade_map:
            base_value = grade_map[base_grade]
            
            # Handle plus/minus modifiers
            if modifier == '+':
                return min(base_value + 3, 100.0)  # Don't exceed 100
            elif modifier == '-':
                return max(base_value - 3, 0.0)    # Don't go below 0
            else:
                return base_value
    
    return None


def convert_to_numeric_grade(grade):
    """
    Convert any grade (numeric or letter) to numeric format.
    
    Args:
        grade: Grade in any format (number, string number, letter)
        
    Returns:
        float: Numeric grade or None if invalid
    """
    # First try to convert as numeric grade
    numeric = get_numeric_grade(grade)
    if numeric is not None:
        return numeric
    
    # If not numeric, try to convert as letter grade
    return letter_to_numeric_grade(grade)


def calculate_grade_distribution(valid_grades):
    """
    Calculate the distribution of letter grades.
    
    Args:
        valid_grades (list): List of valid numeric grades
        
    Returns:
        dict: Distribution of grades with counts and percentages
    """
    # Initialize counters for each grade
    distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    
    # Count each letter grade
    for grade in valid_grades:
        letter = get_letter_grade(grade)
        distribution[letter] += 1
    
    # Calculate percentages
    total_students = len(valid_grades)
    distribution_with_percentages = {}
    
    for letter, count in distribution.items():
        percentage = (count / total_students) * 100 if total_students > 0 else 0
        distribution_with_percentages[letter] = {
            'count': count,
            'percentage': round(percentage, 1)
        }
    
    return distribution_with_percentages

def display_grade_distribution(result):
    """
    Display grade distribution in a nicely formatted way.
    
    Args:
        result (dict): Result from process_grades containing grade_distribution
    """
    if not result or 'grade_distribution' not in result:
        print("No grade distribution data available")
        return
    
    print("📊 Grade Distribution:")
    print("-" * 30)
    
    distribution = result['grade_distribution']
    for letter in ['A', 'B', 'C', 'D', 'F']:
        count = distribution[letter]['count']
        percentage = distribution[letter]['percentage']
        # Create a visual bar
        bar = '█' * int(percentage // 5)  # Each █ represents 5%
        print(f"{letter}: {count:3} students ({percentage:5.1f}%) {bar}")
    
    total = result['total_students']
    print(f"\nTotal Students: {total}")
    print(f"Class Average: {result['average']}")


def get_grade_summary(result):
    """
    Get a summary of class performance.
    
    Args:
        result (dict): Result from process_grades
        
    Returns:
        str: Summary message
    """
    if not result or 'grade_distribution' not in result:
        return "No data available"
    
    distribution = result['grade_distribution']
    total = result['total_students']
    
    passing = distribution['A']['count'] + distribution['B']['count'] + distribution['C']['count'] + distribution['D']['count']
    failing = distribution['F']['count']
    pass_rate = (passing / total) * 100 if total > 0 else 0
    
    avg = result['average']
    
    # Determine class performance level
    if avg >= 90:
        performance = "Excellent"
    elif avg >= 80:
        performance = "Good"
    elif avg >= 70:
        performance = "Satisfactory"
    elif avg >= 60:
        performance = "Below Average"
    else:
        performance = "Poor"
    
    return f"Class Performance: {performance} (Avg: {avg}, Pass Rate: {pass_rate:.1f}%)"


def is_valid_grade(grade):
    """
    Check if a grade is within the acceptable range and is numeric.
    
    Args:
        grade: The grade value to validate
        
    Returns:
        bool: True if grade is a number between 0-100, False otherwise
    """
    return get_numeric_grade(grade) is not None


def process_grades_optimized(grades):
    """
    HIGHLY OPTIMIZED version using list comprehension and built-ins.
    Up to 3x faster for large datasets.
    
    Args:
        grades (list): List of numeric grades (0-100)
        
    Returns:
        dict: Contains average, highest, lowest grades and student count
        None: If no valid grades are found
    """
    # Input validation (fast early return)
    if not isinstance(grades, list) or not grades:
        return None
    
    # SUPER OPTIMIZATION: Single list comprehension handles both numeric and letter grades
    valid_grades = [
        numeric_grade 
        for grade in grades 
        if (numeric_grade := convert_to_numeric_grade(grade)) is not None
    ]
    
    # Early return if no valid grades
    if not valid_grades:
        return None
    
    # All calculations in one go using built-in C functions
    return {
        'average': round(sum(valid_grades) / len(valid_grades), 2),
        'highest': max(valid_grades),
        'lowest': min(valid_grades),
        'total_students': len(valid_grades),
        'grade_distribution': calculate_grade_distribution(valid_grades)
    }

# Test data - Original with Grade Distribution
print("=== Original Test with Grade Distribution ===")
student_grades = [85, 92, 78, 96, 88, 73, 91, 87, 82, 94]
result = process_grades(student_grades)
print("Basic Stats:", {k: v for k, v in result.items() if k != 'grade_distribution'})
print("Grade Distribution:")
for letter, data in result['grade_distribution'].items():
    print(f"  {letter}: {data['count']} students ({data['percentage']}%)")

# Test with more diverse grades to show distribution better
print("\n=== Diverse Grade Distribution Test ===")
diverse_grades = [95, 88, 92, 78, 65, 45, 82, 91, 76, 58, 99, 72, 84, 55, 89]
result2 = process_grades(diverse_grades)
print("Basic Stats:", {k: v for k, v in result2.items() if k != 'grade_distribution'})
print("Grade Distribution:")
for letter, data in result2['grade_distribution'].items():
    print(f"  {letter}: {data['count']} students ({data['percentage']}%)")

print("\n=== Enhanced Grade Distribution Display ===")
display_grade_distribution(result2)
print(f"\n{get_grade_summary(result2)}")

# Test with a failing class
print("\n=== Struggling Class Example ===")
struggling_grades = [45, 55, 32, 78, 65, 48, 52, 41, 69, 58, 38, 61, 44, 56, 73]
struggling_result = process_grades(struggling_grades)
display_grade_distribution(struggling_result)
print(f"\n{get_grade_summary(struggling_result)}")

print("\n=== LETTER GRADE SUPPORT TESTS ===")

# Test 1: Pure letter grades
print("1. Pure letter grades:")
letter_grades = ['A', 'B+', 'B', 'C-', 'A-', 'D+', 'F', 'C', 'B-', 'A+']
letter_result = process_grades(letter_grades)
print(f"Input: {letter_grades}")
display_grade_distribution(letter_result)
print(f"{get_grade_summary(letter_result)}")

# Test 2: Mixed numeric and letter grades
print("\n2. Mixed numeric and letter grades:")
mixed_grades = [95, 'B+', 78, 'A-', 85, 'C', 92, 'D+', 73, 'F']
mixed_result = process_grades(mixed_grades)
print(f"Input: {mixed_grades}")
display_grade_distribution(mixed_result)
print(f"{get_grade_summary(mixed_result)}")

# Test 3: Invalid letter grades
print("\n3. Invalid letter grades handling:")
invalid_letters = ['A', 'B', 'X', 'Z', 'C', 'G', 'D', 'F']
invalid_result = process_grades(invalid_letters)
print(f"Input: {invalid_letters}")
if invalid_result:
    display_grade_distribution(invalid_result)
    print(f"{get_grade_summary(invalid_result)}")

# Test 4: Letter grades with various formats
print("\n4. Various letter grade formats:")
format_grades = ['a', 'B+', 'c-', 'A ', ' D+ ', 'f', 'B-']
format_result = process_grades(format_grades)
print(f"Input: {format_grades}")
if format_result:
    display_grade_distribution(format_result)
    print(f"{get_grade_summary(format_result)}")

print("\n" + "="*60)
print("🔒 COMPREHENSIVE INPUT VALIDATION TESTS")
print("="*60)

# Test 1: Invalid input types
print("\n1. Invalid input types:")
test_cases = [
    ("String instead of list", "85,92,78"),
    ("Integer instead of list", 85),
    ("None input", None),
    ("Dictionary instead of list", {'grades': [85, 92]}),
]

for description, test_input in test_cases:
    result = process_grades(test_input)
    print(f"   {description}: {result.get('error', 'No error')}")

# Test 2: Size validation
print("\n2. Size validation:")
empty_list = []
too_few = [85]  # Less than default minimum
large_list = [85] * 1500  # More than default maximum

print(f"   Empty list: {process_grades(empty_list).get('error', 'No error')}")
print(f"   Too few students: {process_grades(too_few, min_students=3).get('error', 'No error')}")
print(f"   Too many students: {process_grades(large_list, max_students=1000).get('error', 'No error')}")

# Test 3: Mixed valid/invalid data with detailed feedback
print("\n3. Mixed valid/invalid data:")
mixed_invalid = [85, 'B+', None, '', 'X', 150, 'A', -10, '92', 'invalid']
result = process_grades(mixed_invalid)

if 'validation_stats' in result:
    stats = result['validation_stats']
    print(f"   📊 Validation Statistics:")
    print(f"      Total entries: {stats['total_entries']}")
    print(f"      Valid grades: {stats['valid_count']}")
    print(f"      Invalid grades: {stats['invalid_count']}")
    print(f"      Success rate: {stats['success_rate']}%")
    
    if 'warnings' in result:
        print(f"   ⚠️  Warnings: {result['warnings']['message']}")
        print("      Invalid entries:")
        for entry in result['warnings']['invalid_entries']:
            print(f"        Position {entry['position']}: '{entry['value']}' - {entry['suggestion']}")

# Test 4: Suspicious data patterns
print("\n4. Suspicious data patterns:")
identical_data = [85] * 25  # All identical
mostly_none = [85, None, None, None, None, None]
mostly_empty = [85, "", "", "", ""]

print(f"   All identical (25 entries): {process_grades(identical_data).get('warning', 'No warning')}")
print(f"   Mostly None values: {process_grades(mostly_none).get('error', 'No error')}")
print(f"   Mostly empty strings: {process_grades(mostly_empty).get('error', 'No error')}")

# Test 5: Custom validation parameters
print("\n5. Custom validation parameters:")
small_class = [85, 92, 78]
result_custom = process_grades(small_class, max_students=50, min_students=2)
if 'validation_stats' in result_custom:
    print(f"   Small class validation: ✅ Passed (Success rate: {result_custom['validation_stats']['success_rate']}%)")

print(f"\n✨ Enhanced validation provides detailed error messages and statistics!")
print("   - Prevents common input errors")
print("   - Gives helpful suggestions for fixes") 
print("   - Tracks data quality metrics")
print("   - Configurable size limits")

# Test bug fixes
print("\n=== Bug Fix Tests ===")

# Test 1: Mixed data types (previously would crash)
print("1. Mixed data types:")
mixed_grades = [85, 'A', None, 92.5, "invalid", 78]
result = process_grades(mixed_grades)
print(f"   Result: {result}")

# Test 2: All zeros (previously lowest would be wrong)
print("2. All zeros:")
zero_grades = [0, 0, 0]
result = process_grades(zero_grades)
print(f"   Result: {result}")

# Test 3: Empty list
print("3. Empty list:")
empty_grades = []
result = process_grades(empty_grades)
print(f"   Result: {result}")

# Test 4: All invalid grades
print("4. All invalid grades:")
invalid_grades = [150, -10, 200]
result = process_grades(invalid_grades)
print(f"   Result: {result}")

# Test 5: String numbers (should work now)
print("5. String numbers:")
string_grades = ["85", "92", "78"]
result = process_grades(string_grades)
print(f"   Result: {result}")

print("\n=== Performance Comparison ===")
import time

# Test with larger dataset
large_grades = [85, 92, 78, 96, 88, 73, 91, 87, 82, 94] * 1000  # 10,000 grades

# Test original optimized version
start = time.time()
for _ in range(100):
    result1 = process_grades(large_grades)
time1 = time.time() - start

# Test super optimized version
start = time.time()
for _ in range(100):
    result2 = process_grades_optimized(large_grades)
time2 = time.time() - start

print(f"Original optimized: {time1:.4f}s for 100 iterations")
print(f"Super optimized:   {time2:.4f}s for 100 iterations")
print(f"Speedup: {time1/time2:.2f}x faster")
print(f"Results match: {result1 == result2}")

# Test with mixed data types
mixed_large = [85, 'A', None, 92.5, "invalid", 78, -10, 150] * 500
start = time.time()
result3 = process_grades_optimized(mixed_large)
end = time.time()
print(f"\nMixed data test: {end-start:.4f}s")
print(f"Result: {result3}")

print("\n=== Additional Bug Tests ===")

# Bug 1: Single zero treated as falsy
print("6. Single zero grade (BUG):")
single_zero = [0]
result = process_grades(single_zero)
print(f"   Result: {result}")  # Should process, not return None

# Bug 2: Special float values
print("7. Special float values (BUG):")
special_floats = [float('inf'), float('-inf'), float('nan'), 85]
result = process_grades(special_floats)
print(f"   Result: {result}")  # Should only process 85

# Bug 3: Very large numbers that are technically floats
print("8. Very large float:")
large_float = [1e20, 85, 90]  # 1e20 is a huge number
result = process_grades(large_float)
print(f"   Result: {result}")

# Bug 4: Precision issues
print("9. Float precision:")
precision_grades = [33.333333333333336, 66.666666666666664, 100.0]
result = process_grades(precision_grades)
print(f"   Result: {result}")

# Bug 5: Wrong input type (not a list)
print("10. Non-list input:")
not_a_list = "85,92,78"  # String instead of list
result = process_grades(not_a_list)
print(f"   Result: {result}")

# Bug 6: List with one invalid item
print("11. List with just None:")
none_list = [None]
result = process_grades(none_list)
print(f"   Result: {result}")

# Bug 7: Size limit test
print("12. Size limit test:")
large_list = [85] * 15000  # Exceeds default limit of 10000
result = process_grades(large_list)
print(f"   Result: {result}")

# Test: Now we can distinguish different error types
print("\n=== Error Type Distinction ===")
print("Empty list:", process_grades([]))
print("Not a list:", process_grades("not a list"))
print("No valid grades:", process_grades([150, -10, "invalid"]))
print("Valid grades:", process_grades([85, 90]))