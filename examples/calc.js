
/**
 * Calculates the total price with tax.
 *
 * @param {number} amount – Base amount in US dollars.
 * @param {number} taxRate – Tax rate as a decimal (e.g. 0.07 for 7%).
 * @returns {number} Total price including tax.
 */
function calculateTotalPrice(amount, taxRate) {
  return amount + amount * taxRate;
}

