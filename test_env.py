#!/usr/bin/env python
"""Quick test to check environment variables"""
import os

print("=" * 60)
print("ENVIRONMENT VARIABLES TEST")
print("=" * 60)

# Check all environment variables
print("\nAll environment variables:")
for key, value in sorted(os.environ.items()):
    if 'MONGO' in key.upper() or 'DATABASE' in key.upper():
        print(f"  {key} = {value}")

print("\nSpecific checks:")
print(f"  MONGODB_URL = {os.environ.get('MONGODB_URL', 'NOT SET')}")
print(f"  MONGO_HOST = {os.environ.get('MONGO_HOST', 'NOT SET')}")
print(f"  MONGO_PORT = {os.environ.get('MONGO_PORT', 'NOT SET')}")
print(f"  DATABASE_URL = {os.environ.get('DATABASE_URL', 'NOT SET')}")

print("=" * 60)
