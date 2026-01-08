# Walk-in Customer Implementation - Technical Details

## Files Changed

### 1. Views (`app_lumbering_service/views.py`)

#### New Function: `create_walkin_customer`
```python
@login_required
@require_http_methods(["POST"])
def create_walkin_customer(request):
    """Create a new walk-in customer for lumbering service"""
    from app_sales.models import Customer
    
    try:
        name = request.POST.get('name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        
        # Validation
        if not name:
            return JsonResponse({'message': 'Customer name is required'}, status=400)
        if not phone_number:
            return JsonResponse({'message': 'Phone number is required'}, status=400)
        
        # Create customer
        customer = Customer.objects.create(
            name=name,
            phone_number=phone_number,
            email=email or '',
            address=address or '',
        )
        
        return JsonResponse({
            'id': customer.id,
            'name': customer.name,
            'phone_number': customer.phone_number,
        }, status=201)
    
    except Exception as e:
        return JsonResponse({'message': f'Error creating customer: {str(e)}'}, status=500)
```

#### Modified: `lumbering_order_create`
- Added customer validation before order creation
- Returns error if no customer is selected
- Error message displayed in template

### 2. URLs (`app_lumbering_service/urls.py`)

```python
# Walk-in customer creation
path('api/create-walkin-customer/', views.create_walkin_customer, name='api_create_walkin_customer'),
```

### 3. Template (`order_create.html`)

#### HTML Changes
1. **Customer Input Section** (lines 34-45)
   - Changed from `w-full` to `flex gap-2`
   - Added flex container with dropdown and button
   - Button: Green background, white text, plus icon

2. **Modal Dialog** (lines 136-182)
   - Hidden by default (`hidden` class)
   - Fixed positioning over entire page
   - Form with CSRF token
   - Four input fields: name, phone, email, address

3. **Error Display** (lines 16-19)
   - Displays server-side validation errors
   - Red border and background

#### JavaScript Changes
1. **Modal Management** (lines 195-235)
   - Open: Click green button
   - Close: X button, Cancel button, or click outside
   - Auto-focus name field

2. **Form Submission** (lines 237-250)
   - Async POST to `/lumbering/api/create-walkin-customer/`
   - Dynamically add new customer to dropdown
   - Auto-select new customer
   - Reset form and close modal
   - Show success/error toast

3. **Main Form Validation** (lines 205-211)
   - Prevents submission if no customer selected
   - Shows error toast

4. **Toast Notifications** (lines 252-262)
   - Green for success
   - Red for errors
   - Auto-dismisses after 3 seconds

## Data Flow

```
User Click → Open Modal
    ↓
User Fills Form → Validate Client-side
    ↓
User Submits → POST /api/create-walkin-customer/
    ↓
Backend Validates → Check name & phone
    ↓
Create Customer → Save to DB
    ↓
Return JSON → {id, name, phone}
    ↓
Frontend Updates → Add to dropdown
    ↓
Select New Customer → Auto-select
    ↓
Show Success Toast → User continues with order
```

## API Endpoint Details

### POST `/lumbering/api/create-walkin-customer/`

**Request:**
```
Content-Type: application/x-www-form-urlencoded

name=Juan Dela Cruz
phone_number=09123456789
email=juan@example.com
address=123 Main St
csrfmiddlewaretoken=xxxxx
```

**Success Response (201):**
```json
{
  "id": 42,
  "name": "Juan Dela Cruz",
  "phone_number": "09123456789"
}
```

**Error Response (400/500):**
```json
{
  "message": "Error description"
}
```

## Security Measures

1. **CSRF Protection**: All forms include CSRF token
2. **Authentication**: `@login_required` decorator
3. **HTTP Method**: POST only with `@require_http_methods`
4. **Input Sanitization**: `.strip()` on all inputs
5. **Server-side Validation**: Required fields checked
6. **Exception Handling**: Try-except with error response

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Requires JavaScript enabled
- Flex CSS layout support
- Async/await support (ES6)
- Fetch API support

## Performance Considerations

- Minimal server load: Simple INSERT query
- Client-side form validation reduces requests
- Modal doesn't require page reload
- Async request doesn't block UI
- Toast notifications use setTimeout for cleanup

## Error Handling

| Scenario | Handling |
|----------|----------|
| Empty name | 400 + toast message |
| Empty phone | 400 + toast message |
| Network error | Catch block + error toast |
| 500 error | JSON response + error toast |
| Form validation | Client-side alert |

## Testing Endpoints

### Create Walk-in Customer
```bash
curl -X POST http://localhost:8000/lumbering/api/create-walkin-customer/ \
  -H "Cookie: sessionid=xxx; csrftoken=yyy" \
  -d "name=Test Customer&phone_number=09999999999"
```

### Create Service Order
```bash
curl -X POST http://localhost:8000/lumbering/orders/create/ \
  -d "customer=42&wood_type=Mahogany&quantity_logs=5&service_fee_per_bf=5.00&shavings_ownership=lumber_company"
```

## Database Impact

**New Customer Record:**
- `id`: Auto-generated
- `name`: From form
- `phone_number`: From form
- `email`: From form (empty if not provided)
- `address`: From form (empty if not provided)
- `is_senior`: False (default)
- `is_pwd`: False (default)
- `created_at`: Current timestamp
- `updated_at`: Current timestamp

**Lumbering Service Order:**
- `customer`: Foreign key to created customer
- No other changes to existing logic

## Future Enhancements

1. **Duplicate Detection**
   - Check if phone number already exists
   - Warn user before creating duplicate

2. **Customer Search**
   - Fuzzy search in dropdown
   - Quick customer selection

3. **Batch Import**
   - Excel/CSV import for multiple customers
   - Bulk walk-in registration

4. **Customer Validation**
   - Phone number format validation
   - Email verification
   - Address geocoding

5. **Analytics**
   - Track walk-in customer creation rate
   - Peak creation times
   - Customer conversion metrics

6. **Integration**
   - SMS notification to customer
   - Email confirmation
   - CRM integration
   - Loyalty program enrollment

## Maintenance Notes

- Monitor database growth for customer table
- Consider archiving old/inactive customers
- Regular backup of customer data
- Audit trail for customer creation
- GDPR compliance for personal data

## Documentation References

- `WALKIN_CUSTOMER_LUMBERING.md` - Full feature documentation
- `WALKIN_CUSTOMER_QUICK_START.md` - User guide
- Django Forms: https://docs.djangoproject.com/en/stable/topics/forms/
- Django Views: https://docs.djangoproject.com/en/stable/topics/http/views/
- Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
