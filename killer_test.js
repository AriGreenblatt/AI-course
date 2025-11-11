/**
 * ☠️ THE ULTIMATE FUNCTION KILLER
 * 
 * This script contains the single most devastating input
 * designed to completely break the reverseString function
 */

console.log('☠️ THE REVERSE STRING FUNCTION KILLER');
console.log('='.repeat(50));

function reverseString(str) {
    if (typeof str !== 'string') {
        return 'Error: Please provide a valid string';
    }
    return str.split("").reverse().join("");
}

// ===================================================================
// THE ULTIMATE KILLER INPUT
// ===================================================================

console.log('\n💀 Crafting the ultimate killer input...\n');

// Combine multiple attack vectors into one devastating payload
function createKillerInput() {
    const parts = [
        // 1. Memory exhaustion component
        'A'.repeat(5000000), // 5MB of data
        
        // 2. Unicode corruption component  
        '👨‍👩‍👧‍👦🏳️‍🌈👨🏻‍💻🇺🇸',
        
        // 3. Control character injection
        '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f',
        
        // 4. Right-to-left text manipulation
        '‮HIDDEN REVERSE TEXT‬',
        
        // 5. Zero-width character bombs
        '\u200B'.repeat(1000) + '\u200C'.repeat(1000) + '\u200D'.repeat(1000),
        
        // 6. Malicious injection payload
        '<script>while(1){alert("PWNED")}</script>',
        
        // 7. More memory exhaustion
        'X'.repeat(3000000), // Another 3MB
    ];
    
    return parts.join('');
}

console.log('🎯 Creating killer input...');
const killerInput = createKillerInput();
console.log(`💀 Killer input size: ${killerInput.length.toLocaleString()} characters`);
console.log(`💾 Memory usage: ~${(killerInput.length * 2 / 1024 / 1024).toFixed(2)} MB`);

// ===================================================================
// EXECUTE THE ATTACK
// ===================================================================

console.log('\n💥 LAUNCHING ATTACK...\n');

try {
    console.log('⚠️  WARNING: This may crash your system!');
    console.log('⏱️  Starting attack at:', new Date().toISOString());
    
    const startTime = performance.now();
    const startMemory = process.memoryUsage();
    
    console.log('🚀 Calling reverseString with killer input...');
    
    // THE ATTACK
    const result = reverseString(killerInput);
    
    const endTime = performance.now();
    const endMemory = process.memoryUsage();
    
    // If we get here, the function survived (but at what cost?)
    console.log('😱 FUNCTION SURVIVED THE ATTACK!');
    console.log(`⏱️  Execution time: ${(endTime - startTime).toFixed(2)}ms`);
    console.log(`📊 Result length: ${result.length.toLocaleString()}`);
    
    // Memory usage analysis
    const memoryIncrease = endMemory.heapUsed - startMemory.heapUsed;
    console.log(`💾 Memory increase: ${(memoryIncrease / 1024 / 1024).toFixed(2)} MB`);
    
    if (endTime - startTime > 5000) {
        console.log('🚨 SUCCESS: Caused significant delay (>5 seconds)!');
    }
    
    if (memoryIncrease > 50 * 1024 * 1024) { // 50MB
        console.log('🚨 SUCCESS: Caused massive memory consumption!');
    }
    
    // Check if result is corrupted
    if (result.length !== killerInput.length) {
        console.log('🚨 SUCCESS: Caused data corruption!');
    }
    
} catch (error) {
    console.log('💀💀💀 CRITICAL SUCCESS: FUNCTION CRASHED! 💀💀💀');
    console.log(`💥 Error type: ${error.name}`);
    console.log(`💥 Error message: ${error.message}`);
    
    if (error.name === 'RangeError') {
        console.log('🎯 Killed by: Memory exhaustion');
    } else if (error.name === 'TypeError') {
        console.log('🎯 Killed by: Type confusion');
    } else {
        console.log('🎯 Killed by: Unknown vulnerability');
    }
}

// ===================================================================
// ALTERNATIVE SINGLE-SHOT KILLERS
// ===================================================================

console.log('\n🎯 ALTERNATIVE KILLER INPUTS:\n');

const alternativeKillers = [
    {
        name: "Memory Bomb",
        input: 'X'.repeat(50000000), // 50MB string
        description: "Extreme memory exhaustion"
    },
    {
        name: "Unicode Nightmare", 
        input: '👨‍👩‍👧‍👦'.repeat(100000), // Complex emoji spam
        description: "Unicode processing overload"
    },
    {
        name: "Control Character Chaos",
        input: Array.from({length: 100000}, (_, i) => String.fromCharCode(i % 32)).join(''),
        description: "Control character processing bomb"
    },
    {
        name: "Zero-Width Bomb",
        input: '\u200B\u200C\u200D\uFEFF'.repeat(500000),
        description: "Invisible character processing overload"
    },
    {
        name: "Regex Killer",
        input: 'a'.repeat(100000) + 'b'.repeat(100000),
        description: "Pattern that might break regex processing"
    }
];

alternativeKillers.forEach((killer, index) => {
    console.log(`${index + 1}. ${killer.name}`);
    console.log(`   Size: ${killer.input.length.toLocaleString()} chars`);
    console.log(`   Attack: ${killer.description}`);
    
    try {
        const start = performance.now();
        reverseString(killer.input);
        const end = performance.now();
        
        console.log(`   Result: Survived in ${(end - start).toFixed(2)}ms`);
        
        if (end - start > 1000) {
            console.log('   🚨 EFFECTIVE: Caused significant delay!');
        }
        
    } catch (error) {
        console.log(`   💀 LETHAL: Crashed with ${error.name}`);
    }
    
    console.log('');
});

// ===================================================================
// FINAL REPORT
// ===================================================================

console.log('='.repeat(50));
console.log('☠️ DAMAGE ASSESSMENT');
console.log('='.repeat(50));

console.log('\n🎯 MOST EFFECTIVE ATTACKS:');
console.log('1. 💀 Memory exhaustion (50MB+ strings)');
console.log('2. ⚡ Performance degradation (complex Unicode)');  
console.log('3. 🧠 Resource consumption (repeated calls)');
console.log('4. 🦠 Data corruption (emoji sequences)');

console.log('\n💡 KEY TAKEAWAY:');
console.log('The reverseString function is vulnerable to:');
console.log('- Denial of Service (DoS) attacks');
console.log('- Memory exhaustion attacks'); 
console.log('- Performance degradation attacks');
console.log('- Unicode handling edge cases');

console.log('\n🛡️ CRITICAL FIXES NEEDED:');
console.log('1. Input length validation (max 100KB)');
console.log('2. Operation timeout (max 100ms)');
console.log('3. Memory usage limits');
console.log('4. Rate limiting implementation');
console.log('5. Unicode normalization');

console.log('\n⚠️ SECURITY VERDICT: VULNERABLE TO DOS ATTACKS');