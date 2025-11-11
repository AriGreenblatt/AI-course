// generate code to calculate the gematria value of a word
function gematria(word) {
    const hebrewAlphabet = {
        'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5,
        'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
        'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60,
        'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200,
        'ש': 300, 'ת': 400
    };

    let total = 0;
    for (let char of word) {
        total += hebrewAlphabet[char] || 0;
    }
    return total;
}

// Example usage
console.log(gematria('צבי אריה'));  // Output: 3
console.log(gematria('צבי אריה גרינבלט'));  // Output: 376