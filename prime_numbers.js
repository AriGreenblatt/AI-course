// generate prime numbers up to a given limit
function generatePrimes(limit) {
    const primes = [];
    for (let num = 2; num <= limit; num++) {
        let isPrime = true;
        for (let i = 2; i <= Math.sqrt(num); i++) {
            if (num % i === 0) {
                isPrime = false;
                break;
            }
        }
        if (isPrime) {
            primes.push(num);
        }
    }
    return primes;
}

// Example usage
console.log('Prime numbers up to 30:', generatePrimes(30));
console.log('Prime numbers up to 50:', generatePrimes(50));
console.log('Prime numbers up to 100:', generatePrimes(100));

// Show count of primes
const primesTo100 = generatePrimes(100);
console.log(`\nTotal prime numbers up to 100: ${primesTo100.length}`);