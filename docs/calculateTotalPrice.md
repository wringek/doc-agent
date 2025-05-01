# calculateTotalPrice

Calculate the total price including tax based on the amount.

## Purpose
The `calculateTotalPrice` function is a valuable tool for developers looking to streamline the process of calculating the final price of a product after tax. By taking in the base amount and the applicable tax rate as parameters, this function efficiently computes the total cost, ensuring accuracy and consistency across transactions. This is particularly useful in e-commerce applications, where precise pricing is crucial for maintaining customer trust and compliance with tax regulations. By encapsulating this logic in a reusable function, developers can enhance code maintainability and reduce the likelihood of errors in price calculations.

## Usage
```js
calculateTotalPrice(amount, taxRate);
```

## Arguments
| Name | Type | Description |
| ---- | ---- | ----------- |
| `amount` | number | Base amount in US dollars. |
| `taxRate` | number | Tax rate as a decimal (e.g. 0.07 for 7%). |

## Returns
number – The total price calculated by adding the amount and the tax applied to it.

## Examples
Here are two JavaScript code examples demonstrating how to use the `calculateTotalPrice` function.

This example shows how to calculate the total price of a product with a specified amount and tax rate.

```javascript
const amount = 100; // Price of the product
const taxRate = 0.07; // 7% tax rate

const totalPrice = calculateTotalPrice(amount, taxRate);
console.log(`Total Price: $${totalPrice.toFixed(2)}`); // Output: Total Price: $107.00
```

This example demonstrates calculating the total price for a service with a different amount and tax rate.

```javascript
const amount = 250; // Price of the service
const taxRate = 0.05; // 5% tax rate

const totalPrice = calculateTotalPrice(amount, taxRate);
console.log(`Total Price: $${totalPrice.toFixed(2)}`); // Output: Total Price: $262.50
```
