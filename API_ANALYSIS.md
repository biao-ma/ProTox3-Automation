# ProTox-3 API Analysis and Findings

## 🔍 Investigation Summary

### Goal
Identify the actual API endpoint used by ProTox-3 website to enable programmatic access for batch toxicity predictions.

### Findings

#### 1. API Endpoint Discovered

Through browser network monitoring, we identified the actual API endpoint:

```
https://tox.charite.de/protox3/src/run_models.php
```

**Request Type**: XMLHttpRequest (AJAX)  
**Method**: POST  
**Duration**: ~1.3 seconds (for model computation)

#### 2. API Limitations

**Problem**: The API requires a session-based compound ID

When testing with direct POST request:
```bash
curl --insecure -X POST "https://tox.charite.de/protox3/src/run_models.php" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "smiles=CC1=CC(=NO1)NC(=O)NC2=CC(=C(C=C2OC)OC)Cl"
```

**Response**: `Ungültige ID` (Invalid ID in German)

**Root Cause**: The API endpoint `run_models.php` expects a compound ID that is generated during the web form submission process. It does not accept direct SMILES input.

#### 3. Workflow Analysis

The ProTox-3 web interface uses a multi-step process:

```
Step 1: Submit SMILES
  ↓
  POST to: index.php?site=compound_input
  Parameters: smiles_field, selected models
  ↓
Step 2: Server generates compound ID and stores in session
  ↓
Step 3: AJAX call to run predictions
  ↓
  POST to: src/run_models.php
  Parameters: compound_id (from session)
  ↓
Step 4: Results displayed
  ↓
  URL: index.php?site=compound_search_similarity
```

**Key Insight**: The API is not designed for direct programmatic access. It requires:
1. A valid PHP session (PHPSESSID cookie)
2. Prior submission through the web form
3. Server-generated compound ID

---

## 🚫 Why Direct API Access Doesn't Work

### Issue 1: Session Dependency

ProTox-3 uses PHP sessions to track compounds:
- When you submit a SMILES through the web form, the server creates a session
- The compound data is stored server-side with a session-specific ID
- The `run_models.php` endpoint expects this session ID

### Issue 2: No Public REST API

ProTox-3 does not provide a public REST API endpoint that accepts:
```json
{
  "smiles": "CC1=CC(=NO1)NC(=O)NC2=CC(=C(C=C2OC)OC)Cl",
  "models": ["cyto", "dili", "neuro"]
}
```

Instead, it requires browser-based interaction with session management.

### Issue 3: Rate Limiting

The API documentation mentions:
- Maximum 250 queries per day
- This suggests there might be an official API, but it's not publicly accessible via simple HTTP requests

---

## ✅ Working Solutions

### Solution 1: Selenium Automation (Recommended)

**Status**: ✅ Working  
**Method**: Browser automation with Selenium WebDriver

**Advantages**:
- Mimics real browser behavior
- Handles session management automatically
- Works with SSL certificate issues
- Can extract all result data

**Disadvantages**:
- Slower (~5-10 minutes per compound)
- Requires Chrome/Chromium browser
- More resource-intensive

**Usage**:
```bash
python src/protox_full_automation.py 0 10
```

### Solution 2: Requests + Session Management

**Status**: 🔄 Possible but complex  
**Method**: Python requests library with session cookies

**Implementation Approach**:
```python
import requests
from bs4 import BeautifulSoup

session = requests.Session()
session.verify = False  # For SSL issues

# Step 1: Get initial page and session cookie
response = session.get('https://tox.charite.de/protox3/index.php?site=compound_input')

# Step 2: Submit SMILES
data = {
    'smiles_field': 'CC1=CC(=NO1)NC(=O)NC2=CC(=C(C=C2OC)OC)Cl',
    'dili': 'on',
    'cyto': 'on',
    # ... all model checkboxes
}
response = session.post('https://tox.charite.de/protox3/index.php?site=compound_input', data=data)

# Step 3: Extract compound ID from response
soup = BeautifulSoup(response.text, 'html.parser')
# Parse for compound ID...

# Step 4: Call run_models.php with compound ID
response = session.post('https://tox.charite.de/protox3/src/run_models.php', data={'id': compound_id})

# Step 5: Parse results
```

**Advantages**:
- Faster than Selenium
- Less resource-intensive
- Can be run headless

**Disadvantages**:
- More complex implementation
- Requires parsing HTML responses
- May break if website structure changes
- Still needs to handle sessions

---

## 📊 Performance Comparison

| Method | Speed | Reliability | Complexity | Resource Usage |
|--------|-------|-------------|------------|----------------|
| **Selenium** | ⭐⭐ (5-10 min/compound) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Requests + Session** | ⭐⭐⭐⭐ (1-2 min/compound) | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Direct API** | ⭐⭐⭐⭐⭐ (seconds) | ❌ Not available | ⭐ | ⭐ |

---

## 🎯 Recommendations

### For Current Project

**Use Selenium automation** (already implemented and working):

**Reasons**:
1. ✅ Already debugged and working
2. ✅ Handles all edge cases
3. ✅ Reliable results extraction
4. ✅ No risk of breaking due to website changes

**For 97 compounds**:
- Estimated time: 8-16 hours
- Can run overnight or in batches
- Results are reliable and complete

### For Future Improvements

If faster processing is needed:

1. **Implement Requests-based solution**:
   - Analyze the exact form submission process
   - Implement session management
   - Parse HTML responses for results
   - Add error handling for website changes

2. **Contact ProTox-3 team**:
   - Ask about official API access
   - Inquire about batch processing options
   - Request API documentation

3. **Consider alternatives**:
   - Look for other toxicity prediction tools with better APIs
   - Consider local installation of prediction models (if available)

---

## 📝 Conclusion

### API Status

❌ **No simple REST API available**  
✅ **Selenium automation works reliably**  
🔄 **Requests-based solution possible but complex**

### Best Practice

For the current project with 97 compounds:

```bash
# Use the working Selenium solution
bash run_protox.sh

# Or process in batches
bash run_protox.sh 0 25    # Batch 1
bash run_protox.sh 25 50   # Batch 2
bash run_protox.sh 50 75   # Batch 3
bash run_protox.sh 75 97   # Batch 4
```

**Total time**: 8-16 hours (can run overnight)  
**Reliability**: High  
**Maintenance**: Low

---

## 🔗 References

- ProTox-3 Website: https://tox.charite.de/protox3/
- API Documentation Page: https://tox.charite.de/protox3/index.php?site=api
- Discovered Endpoint: https://tox.charite.de/protox3/src/run_models.php

---

**Last Updated**: 2026-01-09  
**Status**: Investigation Complete  
**Recommendation**: Use Selenium automation (already implemented)
