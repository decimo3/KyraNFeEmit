# Fix ValueError on LIGHT Notes

LIGHT notes do not provide a valid **conformidade** value, so the program previously used the **referencia** field as a fallback.

However, the **referencia** field may contain non-numeric values, causing a `ValueError` when the program attempted to convert it to an integer.

To resolve this issue, the program now uses the **pedido** value as the fallback for **conformidade** when processing LIGHT notes. Since **pedido** is always numeric, this prevents the conversion error and ensures consistent processing.
