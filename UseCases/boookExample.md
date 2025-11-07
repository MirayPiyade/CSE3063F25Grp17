 # Use Case UC1 — Process Sale

 **Scope:** NextGen POS application

 **Level:** User goal

 **Primary actor:** Cashier

 ## Stakeholders and Interests

- **Cashier:** Wants accurate, fast entry, and no payment errors, since cash drawer
	shortages are deducted from their salary.
- **Salesperson:** Wants sales commissions updated.
- **Customer:** Wants a fast, low-effort purchase experience, visible display of entered
	items and prices, and a receipt for returns.
- **Company:** Wants accurate transaction records, payment receivables recorded,
	fault tolerance when remote services are unavailable, and fast updates to
	accounting and inventory.
- **Manager:** Wants quick override operations and tools to debug cashier issues.
- **Government tax agencies:** Want taxes collected for each sale (may be multiple
	agencies: national, state, county).
- **Payment Authorization Service:** Wants correctly formatted authorization requests
	and accurate accounting of payables to the store.

 ## Preconditions

- Cashier is identified and authenticated.

 ## Success guarantee (postconditions)

- Sale is saved.
- Tax is correctly calculated.
- Accounting and inventory are updated.
- Commissions recorded.
- Receipt is generated.
- Payment authorization approvals are recorded.

 ## Main success scenario (basic flow)

1. Customer arrives at POS checkout with goods and/or services to purchase.
2. Cashier starts a new sale.
3. Cashier enters item identifier.
4. System records sale line item and presents item description, price, and running total.
	 Price is calculated from a set of price rules. Cashier repeats steps 3–4 until done.
5. System presents total with taxes calculated.
6. Cashier tells customer the total and asks for payment.
7. Customer pays and system handles payment.
8. System logs completed sale and sends sale + payment information to external
	 Accounting (for accounting and commissions) and Inventory systems (to update
	 inventory).
9. System presents receipt.
10. Customer leaves with receipt and goods (if any).

 ## Extensions (alternative flows)

### a) Manager override (at any time)
1. System enters manager-authorized mode.
2. Manager or cashier performs one manager-mode operation (e.g., cash balance
	 change, resume a suspended sale on another register, void a sale).
3. System reverts to cashier-authorized mode.

### b) System failure / recovery (at any time)
To support recovery and correct accounting, ensure all transaction-sensitive state and
events can be recovered from any step.

1. Cashier restarts system, logs in, and requests recovery of prior state.
2. System reconstructs prior state.

#### b.2a) Anomalies preventing recovery
1. System signals error to cashier, records the error, and enters a clean state.
2. Cashier starts a new sale.

### Resume suspended sale
1. Cashier performs resume operation and enters the sale ID.
2. System displays the state of the resumed sale with subtotal.

If sale not found: System signals error and cashier may start a new sale.

### Tax-exempt status
1. Cashier verifies and enters a tax-exempt status code.
2. System records status for tax calculations.

### Invalid item ID
1. System signals error and rejects entry.
2. Cashier options:
	 - Manually enter the numeric UPC or item ID; system displays description and price.
	 - If no ID but a price exists on the tag, request manager override and enter manual
		 price (system applies standard taxation).
	 - Use Find Product Help or ask an employee for the correct item ID or price.

### Multiple quantity entry
If multiple identical items (e.g., 5 packages), cashier can enter a category identifier
and quantity.

### Manual category/price entry
For items like flowers or cards, cashier enters a special manual category code and the
price.

### Removing (voiding) an item
1. Cashier enters the item identifier to remove it from the sale.
2. System removes the item and displays the updated total.

If item price exceeds cashier void limit: System suggests manager override.

### Cancel or suspend sale
- Cashier may cancel the sale.
- Cashier may suspend the sale: system records it so it can be retrieved on any POS
	register and presents a suspend receipt with line items and sale ID.

### Price override / discount / credit
- Manager approval required to change system-supplied item price; cashier enters the
	manual price after override.
- If external tax service is unavailable, system may try to restart the service. If it
	cannot restart, system signals an error and cashier may manually calculate and
	enter tax or cancel the sale.
- Discount eligibility: cashier enters customer ID and system applies discount rules.
- Customer credit: system applies available credit up to total price and reduces remaining
	credit.

### Payment scenarios

#### Paying by cash
1. Cashier enters cash amount tendered.
2. System presents change due and releases cash drawer.
3. Cashier deposits cash and returns change to customer.
4. System records cash payment.

#### Paying by credit/debit
1. Customer presents card information (card reader or manual entry).
2. System displays payment details for verification; cashier confirms.
3. System sends payment authorization request to external Payment Authorization
	 Service and requests approval.

If external authorization service fails: system signals error and cashier asks for
alternate payment.

On approval: system records credit payment (including approval) and may present a
signature capture mechanism. If paper signature used, cashier stores the receipt in
the cash drawer.

On denial or timeout: system signals appropriate error; cashier requests alternate
payment.

#### Other payment flows
- Paying by check or other methods handled similarly.
- Coupons: cashier records coupons before payment; system reduces price and records
	coupons for accounting. If coupon doesn't match purchased items, system signals an
	error.
- Rebates: system presents rebate forms and receipts.
- Gift receipt: cashier can request gift receipt (no prices shown).
- Printer out of paper: if detected, system signals; cashier replaces paper and reprints.

 ## Special requirements

- Touch-screen UI on a large flat panel monitor; text must be visible from 1 meter.
- Credit authorization response within 30 seconds 90% of the time.
- Robust recovery mechanisms when remote services (inventory, tax) are failing.
- Language internationalization for displayed text.
- Pluggable business rules for steps 3 (item entry) and 7 (payment handling).

 ## Technology and data variations

- Manager override may be via swipe card or entering an authorization code.
- Item identifier may be entered via barcode scanner or keyboard and may use UPC, EAN,
	JAN, or SKU.
- Credit account info may be entered via card reader or keyboard.
- Signature capture currently on paper; digital signature capture is expected to
	become common.

 ## Frequency of occurrence

- Could be nearly continuous.

 ## Open issues

- Tax law variations across jurisdictions.
- Remote service recovery approaches.
- Customization needs for different businesses.
- Operational policies (e.g., must a cashier take their cash drawer when logging out?).
- Can the customer use the card reader directly, or must the cashier handle it?

-----

*Source:* Example: Process Sale (fully dressed style) — original content preserved and
reformatted for clarity.