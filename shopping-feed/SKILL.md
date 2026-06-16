---
name: shopping-feed
description: Optimize Google Shopping feeds for maximum product visibility and ad performance. Use when managing product data, improving feed quality scores, optimizing product titles and attributes, fixing feed errors, implementing GTIN requirements, or integrating with Google Merchant Center API. Covers feed specifications, title optimization, image requirements, and API integration for Shopping campaigns.
---

# Google Shopping Feed Optimization

Optimize Google Shopping feeds to maximize product visibility, meet Google Merchant Center requirements, and improve Shopping campaign performance.

## Product Data Specifications

### Required Attributes

| Attribute | Format | Character Limit | Critical Notes |
|-----------|--------|-----------------|----------------|
| id | Alphanumeric | 50 chars | Use SKU; keep consistent across updates |
| title | Plain text | 150 chars | Only ~70 visible in ads |
| description | Plain text | 5,000 chars | Must match landing page |
| link | URL | 2,000 chars | Must be functional, crawlable |
| image_link | URL | 2,000 chars | High quality required |
| price | Numeric + ISO 4217 | Must match LP | US/Canada exclude taxes |
| availability | Enum | — | in_stock, out_of_stock, preorder, backorder |
| condition | Enum | — | new, refurbished, used |
| brand | Text | 70 chars | Required for most categories |
| gtin | Numeric | 8-14 digits | Required when assigned by manufacturer |
| mpn | Alphanumeric | 70 chars | Manufacturer Part Number |

### Optional but High-Impact Attributes

- **product_type:** Your internal categorization (up to 750 chars)
- **google_product_category:** Google's taxonomy (required for accurate matching)
- **item_group_id:** Groups product variants (color, size) together
- **additional_image_link:** Up to 10 additional images
- **sale_price:** Promotional pricing with dates
- **shipping:** Shipping cost details
- **custom_labels:** 0-4 labels for campaign segmentation

## GTIN Requirements

**When GTIN is required:**
- Products that have manufacturer-assigned GTINs must include them
- Missing GTIN for applicable products = "limited visibility" status
- Products without GTINs (handmade, custom) use `identifier_exists = false`

**Accepted GTIN formats:**
- UPC (12-digit): North America
- EAN (13-digit): Europe
- JAN (8/13-digit): Japan
- ISBN (10/13-digit): Books
- ITF-14 (14-digit): Packaging

**Validation:** GTINs must pass check digit validation. Use online validators before submission.

## Title Optimization Formula

### Structure by Category

**Apparel:**
```
Brand + Gender + Product Type + Color + Size + Material
Example: "Nike Women's Running Shoes Black Size 8 Mesh"
```

**Electronics:**
```
Brand + Model Number + Product Type + Key Specs
Example: "Samsung 55-Inch 4K Smart TV UN55TU8000"
```

**Beauty:**
```
Brand + Product Name + Size/Volume
Example: "L'Oreal Revitalift Serum 30ml"
```

### Title Best Practices

**Front-load keywords:** First 70 characters are visible in ads
**Prioritize:**
1. Brand (builds trust)
2. Most searched attributes (varies by product)
3. Differentiating features
4. Size/quantity

**Avoid:**
- ALL CAPS (except acronyms)
- Promotional text ("FREE SHIPPING", "SALE")
- Special characters (★, ☆, →)
- Generic terms without specifics ("Great Product")

**Performance impact:** Well-optimized titles achieve 2-3x CTR improvement. A/B tested titles show up to 700% CTR improvement in case studies.

### Title Length Strategy

- **Short titles (40-60 chars):** Mobile-optimized, clear, concise
- **Medium titles (70-100 chars):** Desktop balance of detail and readability
- **Long titles (100-150 chars):** Maximum detail for specific queries

## Image Requirements

### Technical Specifications

| Product Type | Minimum Size | Recommended | Maximum File Size |
|--------------|--------------|-------------|-------------------|
| Non-apparel | 100×100 px | 800-1500 px | 16 MB |
| Apparel | 250×250 px | 1500×1500 px | 16 MB |

**Aspect ratio:** Square (1:1) or close to square recommended
**Format:** JPEG, PNG, GIF, BMP, TIFF, WebP
**Color space:** RGB or CMYK

### Image Quality Guidelines

**Product positioning:**
- Product occupies 75-90% of image frame
- Clear, well-lit, high resolution
- Multiple angles via additional_image_link

**Background:**
- White or neutral solid color recommended
- Lifestyle images acceptable but product must be clear
- No watermarks, promotional text, logos, borders

**Prohibited:**
- Placeholder images
- Images with text overlay (prices, "NEW", "SALE")
- Collages (unless showing product variations)
- Blurry or pixelated images

## Google Merchant Center API Integration

### Content API for Shopping

**Note:** Being replaced by Merchant API. Both available during transition.

**Key operations:**
- `products.insert` — Add or update single product
- `products.delete` — Remove product from feed
- `products.custombatch` — Batch operations (up to 1,000 products)
- `productstatuses` — Check product approval/disapproval status

### API Example: Product Insert

```python
from googleapiclient.discovery import build

service = build('content', 'v2.1', credentials=credentials)

product = {
    'offerId': 'SKU12345',
    'title': 'Nike Women\'s Running Shoes Black Size 8',
    'description': 'Comfortable running shoes with cushioned sole...',
    'link': 'https://example.com/product/sku12345',
    'imageLink': 'https://example.com/images/sku12345.jpg',
    'price': {'value': '89.99', 'currency': 'USD'},
    'availability': 'in_stock',
    'condition': 'new',
    'brand': 'Nike',
    'gtin': '00012345678905',
    'googleProductCategory': 'Apparel & Accessories > Shoes',
    'productTypes': ['Apparel > Shoes > Athletic Shoes > Running Shoes']
}

request = service.products().insert(
    merchantId=merchant_id,
    body=product
)
response = request.execute()
```

### Supplemental Feeds

Use supplemental feeds for partial updates without affecting other attributes or resetting expiration dates:

**Use cases:**
- Price updates only
- Availability changes
- Sale price modifications
- Inventory quantity updates

**Benefits:**
- Faster updates (don't need to resubmit entire feed)
- Lower API call volume
- No risk of overwriting other attributes

**Minimum update interval:** 30 minutes
**Product expiration:** 30 days without updates

## Feed Error Resolution

### Common Feed Issues

**1. Missing required attributes**
- Error: "Missing value [title]"
- Fix: Ensure all required fields populated
- Prevention: Validate feed schema before submission

**2. Price mismatch**
- Error: "Price on website does not match feed"
- Fix: Sync feed price with landing page exactly
- Prevention: Automated price sync scripts

**3. Out of stock products**
- Error: "Landing page not available"
- Fix: Update availability to 'out_of_stock' or remove from feed
- Prevention: Real-time inventory sync

**4. Image quality issues**
- Error: "Image too small" or "Image quality insufficient"
- Fix: Upload higher resolution images (800px+ minimum)
- Prevention: Validate image dimensions during upload

**5. Incorrect GTIN**
- Error: "Invalid GTIN" or "GTIN doesn't match product"
- Fix: Verify GTIN accuracy, use identifier_exists=false if no GTIN
- Prevention: GTIN validation during product data entry

### Feed Quality Score

Google assigns quality score based on:
- Complete and accurate data
- High-quality images
- Competitive pricing
- Product availability accuracy
- Landing page experience

**Impact:** Higher quality scores = better ad placement and lower CPCs

## Performance Benchmarks (2024)

### Shopping Campaign Averages

| Metric | Average | Strong | Excellent |
|--------|---------|--------|-----------|
| CTR | 0.86% | 1.2%+ | 1.5%+ |
| CPC | $0.66 | <$0.50 | <$0.40 |
| CVR | 1.91% | 3%+ | 4%+ |
| CPA | $38.87 | <$30 | <$20 |

**Industry variation:** Fashion/apparel typically higher CTR (1.2%+), electronics higher CPC ($0.80+)

## Feed Optimization Workflow

### Weekly Tasks
- Monitor feed processing status
- Review disapproved products
- Update prices to match website
- Check inventory sync accuracy

### Monthly Deep Dive
1. Title optimization A/B testing
2. Image quality audit
3. Attribute completeness review
4. Competitive price analysis
5. Category mapping validation

### Quarterly Strategy
1. Full feed audit
2. Product taxonomy optimization
3. Custom label strategy refinement
4. Seasonal product preparation
5. Historical performance analysis

## Automation Opportunities

### Automated Feed Management

**Price monitoring:**
- Scrape competitor prices
- Alert when prices are uncompetitive
- Auto-adjust sale_price for promotions

**Inventory sync:**
- Real-time stock level updates
- Auto-update availability field
- Prevent ad spend on out-of-stock items

**Title optimization:**
- Generate titles from product attributes
- A/B test title variations
- Apply winning formulas automatically

### API-Driven Updates

```python
# Pseudocode for automated feed management
products = get_all_products()

for product in products:
    # Price sync
    website_price = scrape_price(product.landing_page)
    if product.price != website_price:
        update_product_price(product.id, website_price)
    
    # Inventory sync
    stock_level = get_inventory(product.sku)
    if stock_level == 0 and product.availability != 'out_of_stock':
        update_availability(product.id, 'out_of_stock')
    
    # Title optimization
    if product.title_performance < benchmark:
        new_title = optimize_title(product)
        test_title_variation(product.id, new_title)
```

## Integration with Other Skills

- **pmax-auditor:** Shopping feed quality impacts PMax campaign performance
- **search-terms:** Use search term insights to optimize product titles
- **rsa-generator:** Apply title optimization principles to ad copy

For feed templates by vertical, see references/feed-templates.md
For API integration guide, see references/merchant-center-api.md
For GTIN validation tools, see scripts/gtin-validator.py
