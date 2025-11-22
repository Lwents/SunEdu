#!/bin/bash
# Test script for start attempt API
# Usage: ./test_start_attempt.sh [token] [exercise_id] [student_id]

BASE_URL="http://127.0.0.1:8000/api"
TOKEN="${1:-your_token_here}"
EXERCISE_ID="${2:-d88b35b3-fb55-44b8-9c0d-0eedb821d649}"
STUDENT_ID="${3:-3}"

echo "Testing Start Attempt API"
echo "=========================="
echo "Exercise ID: $EXERCISE_ID"
echo "Student ID: $STUDENT_ID"
echo ""

# Test 1: Start attempt (should fail if already finished)
echo "Test 1: POST /activities/exercises/$EXERCISE_ID/start/"
echo "----------------------------------------"
curl -X POST "$BASE_URL/activities/exercises/$EXERCISE_ID/start/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -v

echo ""
echo ""

# Test 2: Get attempt summary (if attempt exists)
echo "Test 2: GET /activities/attempts/{attempt_id}/"
echo "----------------------------------------"
ATTEMPT_ID="61e9558e-f6ca-4294-bb8b-505b8edce828"
curl -X GET "$BASE_URL/activities/attempts/$ATTEMPT_ID/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -v

echo ""
echo "Done!"

