// generate a function that calculates the MD5 hash of a given string
// without using calculateMD5 function
function calculateMD5(str) {
	// Simple MD5 implementation using crypto module (Node.js)
	const crypto = require('crypto');
	return crypto.createHash('md5').update(str).digest('hex');
/**
 * Calculates the MD5 hash of a given string.
 * @param {string} str - The input string to hash.
 * @returns {string} The MD5 hash of the input string.
 */
    function calculateMD5(str) {
        // Example usage
        console.log(calculateMD5('Hello World'));  // Output: 5eb63bbbe01eeed093cb22bb8f5acdc3
        console.log(calculateMD5('OpenAI'));       // Output: 2c6ee24b09816a6f14f95d1698b24ead
    }