# Implementation of LIGHT Business Rules

## Fix ValueError on LIGHT Notes

LIGHT notes do not provide a valid **conformidade** value, so the program previously used the **referencia** field as a fallback.

However, the **referencia** field may contain non-numeric values, causing a `ValueError` when the program attempted to convert it to an integer.

To resolve this issue, the program now uses the **pedido** value as the fallback for **conformidade** when processing LIGHT notes. Since **pedido** is always numeric, this prevents the conversion error and ensures consistent processing.

## Fix KeyError on Retained ISSQN Validation

An incorrect property was used when calculating the expected retained ISSQN value during validation. The calculation has been updated to use the correct property, ensuring accurate verification and preventing `KeyError` exceptions.

## Brazilian Number Formatting

Normalized numeric values now follow Brazilian formatting conventions, including thousands separators in addition to decimal separators.

Example:

* Previous format: `1234,56`
* New format: `1.234,56`

This change improves readability and aligns the generated values with local standards and user expectations.
