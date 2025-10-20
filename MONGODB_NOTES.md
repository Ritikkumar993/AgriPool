# MongoDB with MongoEngine - Important Notes

## Key Differences from SQL Databases

### 1. No JOIN Operations
MongoDB is a NoSQL database and doesn't support SQL-style JOINs. When using MongoEngine with Django, you cannot use double-underscore lookups across multiple references.

#### ❌ This Won't Work:
```python
# Trying to filter across two references (join)
plans = FertilizerPlan.objects.filter(parcel__farmer=farmer)
```

**Error**: `InvalidQueryError: Cannot perform join in mongoDB: parcel__farmer`

#### ✅ This Works:
```python
# First get the intermediate objects
parcels = Parcel.objects.filter(farmer=farmer)
parcel_ids = [parcel.id for parcel in parcels]

# Then filter using the IDs
plans = FertilizerPlan.objects.filter(parcel__in=parcel_ids)
```

### 2. Reference Field Queries

You can query one level deep with ReferenceFields:

#### ✅ Single Level Reference (Works):
```python
# Direct reference query
parcels = Parcel.objects.filter(farmer=farmer)
shipments = Shipment.objects.filter(farmer=farmer)
```

#### ❌ Multi-Level Reference (Doesn't Work):
```python
# Trying to go through multiple references
plans = FertilizerPlan.objects.filter(parcel__farmer=farmer)
```

### 3. Workarounds for Complex Queries

#### Option 1: Two-Step Query (Recommended)
```python
# Step 1: Get intermediate objects
parcels = Parcel.objects.filter(farmer=farmer)

# Step 2: Extract IDs and query
parcel_ids = [p.id for p in parcels]
plans = FertilizerPlan.objects.filter(parcel__in=parcel_ids)
```

#### Option 2: Manual Filtering
```python
# Get all plans and filter in Python
all_plans = FertilizerPlan.objects.all()
farmer_plans = [p for p in all_plans if p.parcel.farmer == farmer]
```

**Note**: Option 1 is more efficient for large datasets.

### 4. Aggregation Pipelines

For complex queries, use MongoDB's aggregation framework:

```python
from mongoengine import Q

# Use Q objects for complex queries
results = Model.objects(
    Q(field1=value1) | Q(field2=value2)
)
```

### 5. Best Practices

1. **Design for MongoDB**: Structure your data to minimize cross-collection queries
2. **Denormalize when needed**: Store frequently accessed data together
3. **Use IDs for filtering**: Extract IDs first, then filter
4. **Avoid deep nesting**: Keep reference chains shallow
5. **Consider embedding**: For one-to-few relationships, embed documents instead of referencing

### 6. Common Patterns

#### Pattern 1: Get Related Objects
```python
# Get all shipments for a farmer's parcels
parcels = Parcel.objects.filter(farmer=farmer)
parcel_ids = [p.id for p in parcels]
shipments = Shipment.objects.filter(parcel__in=parcel_ids)
```

#### Pattern 2: Count Related Objects
```python
# Count fertilizer plans for farmer
parcels = Parcel.objects.filter(farmer=farmer)
parcel_ids = [p.id for p in parcels]
plans_count = FertilizerPlan.objects.filter(parcel__in=parcel_ids).count()
```

#### Pattern 3: Filter with Multiple Conditions
```python
# Get available transport offers for specific route
offers = TransportOffer.objects.filter(
    from_location__icontains='Pune',
    to_location__icontains='Mumbai',
    status='available'
)
```

## Fixed Issues in This Project

### Issue 1: Farmer Dashboard
**Problem**: Tried to filter FertilizerPlan by `parcel__farmer`

**Solution**: 
```python
# Before (broken)
plans = FertilizerPlan.objects.filter(parcel__farmer=farmer)

# After (working)
parcel_ids = [parcel.id for parcel in parcels]
plans = FertilizerPlan.objects.filter(parcel__in=parcel_ids)
```

## Resources

- [MongoEngine Documentation](http://docs.mongoengine.org/)
- [MongoDB Query Operators](https://docs.mongodb.com/manual/reference/operator/query/)
- [Django + MongoDB Best Practices](https://www.mongodb.com/compatibility/mongodb-and-django)

## Summary

When working with MongoDB and MongoEngine:
- ✅ Single-level reference queries work fine
- ❌ Multi-level joins don't work
- ✅ Use two-step queries with ID lists
- ✅ Consider data structure design to minimize cross-collection queries
