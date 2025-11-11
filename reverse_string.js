// reverse a string

/*
Function Signature Completion with Copilot
Learning Objective
Learn how function signatures and docstrings help Copilot generate accurate function implementations.

Instructions
Create a new Python file called string_utils.py
Write function signatures with descriptive names and type hints
Add docstrings explaining the function's purpose
Let Copilot complete the function bodies
Test the generated functions
Your Task
Create the following function signatures and let Copilot implement them:

def reverse_string(text: str) -> str:
    """
    Reverses the input string.

    Args:
        text: The string to reverse

    Returns:
        The reversed string
    """
    # Let Copilot complete this

def count_vowels(text: str) -> int:
    """
    Counts the number of vowels (a, e, i, o, u) in the input string.
    Case insensitive.

    Args:
        text: The string to analyze

    Returns:
        The number of vowels found
    """
    # Let Copilot complete this

def is_palindrome(text: str) -> bool:
    """
    Checks if a string reads the same forwards and backwards.
    Ignores spaces and case.

    Args:
        text: The string to check

    Returns:
        True if palindrome, False otherwise
    """
    # Let Copilot complete this
What You'll Learn
How function signatures guide Copilot's understanding
The power of good docstrings for generating accurate code
How type hints improve suggestion quality
The importance of clear function naming
Success Criteria
 All functions work as described in their docstrings
 Copilot generates logical implementations
 You understand how signatures influence suggestions
 Functions handle edge cases appropriately
Test Your Functions
Add these test cases to verify your functions work:

# Test cases
print(reverse_string("hello"))  # Should print "olleh"
print(count_vowels("Hello World"))  # Should print 3
print(is_palindrome("A man a plan a canal Panama"))  # Should print True
*/

function reverseString(str) {
    // Check if input is valid
    if (typeof str !== 'string') {
        return 'Error: Please provide a valid string';
    }
    
    return str.split("").reverse().join("");
}

// Nice interface with examples and demonstrations
console.log('='.repeat(50));
console.log('🔄 STRING REVERSER PROGRAM 🔄');
console.log('='.repeat(50));

// Example demonstrations
const examples = [
    'Hello World',
    'JavaScript',
    'OpenAI',
    '12345',
    'A man a plan a canal Panama',
    'racecar'
];

console.log('\n📝 Example demonstrations:');
console.log('-'.repeat(30));

examples.forEach((example, index) => {
    const reversed = reverseString(example);
    console.log(`${index + 1}. "${example}" → "${reversed}"`);
});

// Show palindrome detection
console.log('\n🔄 Palindrome Check:');
console.log('-'.repeat(30));

examples.forEach(example => {
    const reversed = reverseString(example);
    const isPalindrome = example.toLowerCase().replace(/\s/g, '') === 
                        reversed.toLowerCase().replace(/\s/g, '');
    console.log(`"${example}" ${isPalindrome ? '✅ is' : '❌ is not'} a palindrome`);
});

// Interactive section (simulated)
console.log('\n🎯 Custom Examples:');
console.log('-'.repeat(30));

const customTests = [
    'The quick brown fox',
    'Never odd or even',
    'Was it a car or a cat I saw?'
];

customTests.forEach(test => {
    const reversed = reverseString(test);
    console.log(`Input:  "${test}"`);
    console.log(`Output: "${reversed}"`);
    console.log('');
});

console.log('='.repeat(50));
console.log('✨ Program completed successfully! ✨');
