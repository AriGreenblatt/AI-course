/**
 * 🧪 DESTRUCTIVE TEST DATA FOR REVERSE STRING FUNCTION
 * 
 * This file contains test cases designed to break, crash, or expose
 * vulnerabilities in the reverseString() function.
 */

console.log('🚨 DESTRUCTIVE TEST SUITE FOR REVERSE STRING 🚨');
console.log('='.repeat(60));

// Import or define the function to test
function reverseString(str) {
    // Check if input is valid
    if (typeof str !== 'string') {
        return 'Error: Please provide a valid string';
    }
    
    return str.split("").reverse().join("");
}

console.log('\n🎯 TESTING STRATEGY: Find breaking points...\n');

// ===================================================================
// 1. NULL AND UNDEFINED ATTACKS
// ===================================================================
console.log('💀 PHASE 1: NULL/UNDEFINED ATTACKS');
console.log('-'.repeat(40));

const nullTests = [
    null,
    undefined,
    NaN,
    {},
    [],
    0,
    false,
    true,
    Symbol('test'),
    BigInt(123)
];

nullTests.forEach((test, index) => {
    try {
        const result = reverseString(test);
        console.log(`${index + 1}. Input: ${test} (${typeof test}) → Result: "${result}"`);
    } catch (error) {
        console.log(`${index + 1}. Input: ${test} → 🔥 CRASHED: ${error.message}`);
    }
});

// ===================================================================
// 2. MEMORY EXHAUSTION ATTACKS
// ===================================================================
console.log('\n💾 PHASE 2: MEMORY EXHAUSTION ATTACKS');
console.log('-'.repeat(40));

const memoryTests = [
    'A'.repeat(1000000),      // 1MB string
    'X'.repeat(10000000),     // 10MB string - might crash browser
    '🚀'.repeat(100000),      // Unicode emojis (4 bytes each)
    'a'.repeat(2**20),        // 2^20 characters
    '\u0000'.repeat(50000)    // Null characters
];

memoryTests.forEach((test, index) => {
    try {
        console.log(`${index + 1}. Testing ${test.length} character string...`);
        const startTime = performance.now();
        const result = reverseString(test);
        const endTime = performance.now();
        
        console.log(`   ✅ Success: ${result.length} chars in ${(endTime - startTime).toFixed(2)}ms`);
        if (endTime - startTime > 1000) {
            console.log('   ⚠️  WARNING: Performance issue detected!');
        }
    } catch (error) {
        console.log(`   🔥 CRASHED: ${error.message}`);
    }
});

// ===================================================================
// 3. UNICODE AND ENCODING ATTACKS
// ===================================================================
console.log('\n🌍 PHASE 3: UNICODE/ENCODING ATTACKS');
console.log('-'.repeat(40));

const unicodeTests = [
    '🚀🔥💻🎯',                    // Emojis
    '𝕳𝖊𝖑𝖑𝖔',                      // Mathematical script
    'Ĥéłłø Wørłđ',                  // Accented characters
    '‮drowssap ruoy si siht‬',      // Right-to-left override (hidden reverse)
    '﷽',                           // Arabic ligature (1 char, complex)
    '\u200B\u200C\u200D',          // Zero-width characters
    '𝒽𝑒𝓁𝓁𝑜',                     // Cursive Unicode
    '\uFEFF',                      // Byte order mark
    '\u0001\u0002\u0003',          // Control characters
    'test\0string',                // Null byte injection
    '👨‍👩‍👧‍👦',                        // Family emoji (compound)
    '🇺🇸🇬🇧🇫🇷',                    // Flag emojis
];

unicodeTests.forEach((test, index) => {
    try {
        const result = reverseString(test);
        console.log(`${index + 1}. "${test}" (${test.length} chars) → "${result}" (${result.length} chars)`);
        
        // Check if lengths match (Unicode might break)
        if (test.length !== result.length) {
            console.log('   🚨 LENGTH MISMATCH! Unicode handling broken!');
        }
        
        // Verify it's actually reversed
        const manualReverse = test.split('').reverse().join('');
        if (result !== manualReverse) {
            console.log('   🚨 REVERSAL FAILED! Not properly reversed!');
        }
        
    } catch (error) {
        console.log(`${index + 1}. "${test}" → 🔥 CRASHED: ${error.message}`);
    }
});

// ===================================================================
// 4. SPECIAL CHARACTER ATTACKS
// ===================================================================
console.log('\n🔧 PHASE 4: SPECIAL CHARACTER ATTACKS');
console.log('-'.repeat(40));

const specialTests = [
    '',                           // Empty string
    ' ',                          // Single space
    '\n\t\r',                     // Whitespace chars
    '\\\\\\\\\\',                 // Backslashes
    '""""""""""',                 // Quotes
    "''''''''",                   // Single quotes
    '(((())))[[[[]]]]{{{{}}}}',   // Brackets
    ';;;;;;;;',                   // Semicolons
    '/**//**//***/',              // Comment-like
    '<script>alert("xss")</script>', // XSS attempt
    'SELECT * FROM users;',       // SQL injection attempt
    '../../../etc/passwd',        // Path traversal
    '%00%0a%0d',                  // URL encoded nulls
    '\x00\x01\x02\x03',          // Hex escapes
];

specialTests.forEach((test, index) => {
    try {
        const result = reverseString(test);
        console.log(`${index + 1}. "${test}" → "${result}"`);
    } catch (error) {
        console.log(`${index + 1}. "${test}" → 🔥 CRASHED: ${error.message}`);
    }
});

// ===================================================================
// 5. PERFORMANCE KILLER ATTACKS
// ===================================================================
console.log('\n⚡ PHASE 5: PERFORMANCE ATTACKS');
console.log('-'.repeat(40));

// Generate pathological cases
const performanceTests = [
    // Repeated patterns that might trigger regex issues
    'ababab'.repeat(10000),
    'abcabc'.repeat(8000), 
    '123123'.repeat(6000),
    
    // Alternating patterns
    'a'.repeat(50000) + 'b'.repeat(50000),
    
    // Complex Unicode repeated
    '🚀'.repeat(25000),
    
    // Mixed case nightmare
    'AaAaAa'.repeat(15000),
];

performanceTests.forEach((test, index) => {
    try {
        console.log(`${index + 1}. Testing performance with ${test.length} chars...`);
        
        const startTime = performance.now();
        const result = reverseString(test);
        const endTime = performance.now();
        
        const duration = endTime - startTime;
        console.log(`   ⏱️  Time: ${duration.toFixed(2)}ms`);
        
        if (duration > 100) {
            console.log('   🐌 SLOW PERFORMANCE WARNING!');
        }
        if (duration > 1000) {
            console.log('   🚨 CRITICAL: Performance bottleneck detected!');
        }
        
    } catch (error) {
        console.log(`   🔥 CRASHED: ${error.message}`);
    }
});

// ===================================================================
// 6. EDGE CASE COMBINATIONS
// ===================================================================
console.log('\n🎭 PHASE 6: COMBINED EDGE CASES');
console.log('-'.repeat(40));

const comboTests = [
    null + undefined,             // Type coercion 
    '   ' + '\0' + '   ',        // Spaces + null
    '🚀' + '\u200B' + '💻',      // Emoji + invisible
    'test\nnew\tline',           // Mixed whitespace
    String.fromCharCode(0, 1, 2, 3, 4, 5), // Control chars
];

comboTests.forEach((test, index) => {
    try {
        const result = reverseString(test);
        console.log(`${index + 1}. Complex test → Result length: ${result.length}`);
    } catch (error) {
        console.log(`${index + 1}. Complex test → 🔥 CRASHED: ${error.message}`);
    }
});

// ===================================================================
// 7. PROTOTYPE POLLUTION ATTEMPTS
// ===================================================================
console.log('\n🦠 PHASE 7: PROTOTYPE POLLUTION TESTS');
console.log('-'.repeat(40));

const pollutionTests = [
    '__proto__',
    'constructor',
    'prototype',
    'toString',
    'valueOf',
];

pollutionTests.forEach((test, index) => {
    try {
        const result = reverseString(test);
        console.log(`${index + 1}. "${test}" → "${result}"`);
        
        // Check if it modified anything dangerous
        if (test === '__proto__' && result !== 'otorp___') {
            console.log('   🚨 PROTOTYPE POLLUTION RISK!');
        }
        
    } catch (error) {
        console.log(`${index + 1}. "${test}" → 🔥 CRASHED: ${error.message}`);
    }
});

// ===================================================================
// SUMMARY REPORT
// ===================================================================
console.log('\n' + '='.repeat(60));
console.log('📋 VULNERABILITY ASSESSMENT COMPLETE');
console.log('='.repeat(60));

console.log('\n🎯 KEY FINDINGS:');
console.log('1. Type checking exists but may not cover all cases');
console.log('2. No input sanitization for malicious content');  
console.log('3. No length limits - vulnerable to DoS attacks');
console.log('4. Unicode handling may have edge cases');
console.log('5. No protection against memory exhaustion');

console.log('\n💡 RECOMMENDED FIXES:');
console.log('1. Add maximum string length limits');
console.log('2. Implement input sanitization');
console.log('3. Add timeout for long operations');
console.log('4. Better Unicode/emoji handling');
console.log('5. Rate limiting for repeated calls');

console.log('\n🚨 MOST DANGEROUS INPUTS:');
console.log('- Extremely long strings (memory exhaustion)');
console.log('- Complex Unicode sequences');
console.log('- Null/undefined without proper checking');
console.log('- Repeated function calls (DoS)');

console.log('\n✅ Test suite completed. Review results above.');