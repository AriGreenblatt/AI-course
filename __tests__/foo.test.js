const foo = require('../foo');

test('foo should return true when input is valid', () => {
	expect(foo('valid input')).toBe(true);
});

test('foo should return false when input is invalid', () => {
	expect(foo('invalid input')).toBe(false);
});