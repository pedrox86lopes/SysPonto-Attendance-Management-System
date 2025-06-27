docs/api/endpoints.md - Complete API Endpoints Reference
========================================================

API Endpoints
=============

Complete reference for all SysPonto API endpoints based on the actual Django implementation.

📋 Base Information
-------------------

*   **Base URL**: http://localhost:8000 (development)
    
*   **Authentication**: Session-based with CSRF protection
    
*   **Content-Type**: application/x-www-form-urlencoded for most endpoints
    
*   **Response Format**: JSON
    

🔑 Attendance Management
------------------------

### Generate Attendance Code

Generate a new attendance code for a class session.


**Authentication**: Teacher role required

**Parameters**:



**Response**:


**Error Responses**:


**Example**:


### Submit Attendance Code

Submit an attendance code as a student.


**Authentication**: Student role required

**Parameters**:


**Response**:


**Error Responses**:


**Example**:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashcurl -X POST http://localhost:8000/api/submit-attendance/ \    -b cookies.txt \    -H "X-CSRFToken: your_csrf_token" \    -d "attendance_code=ABC123&simulated_latitude=41.5369&simulated_longitude=-8.4239"   `

### Run AI Validation

Trigger AI validation for an attendance record.


**Authentication**: Teacher role required

**Parameters**:


**Response**:


### Validate Attendance

Mark an attendance record as present (teacher validation).


**Authentication**: Teacher role required

**Parameters**:


**Response**:


### Get Session Submissions

Retrieve all attendance submissions for a class session.


**Authentication**: Teacher role required

**Parameters**:


**Response**:


📝 Absence Justification
------------------------

### Submit Justification

Submit an absence justification with optional document.


**Authentication**: Student role required

**Content-Type**: multipart/form-data

**Parameters**:


**Response**:


**Error Responses**:


👥 Student Dashboard APIs
-------------------------

### Get Current Classes


**Authentication**: Student role required

**Response**:


### Get Today's Classes


**Authentication**: Student role required

**Response**:


### Get Weekly Classes

**Authentication**: Student role required

**Response**:


### Get Attendance History

Get student's attendance history.


**Authentication**: Student role required

**Parameters**:


**Response**:

🏫 Admin Management APIs
------------------------

_Note: These APIs are implemented in the admin\_views.py file but may require additional URL configuration_

### Create User


**Authentication**: Administrator role required

**Parameters**:


**Response**:


### Create Course


**Authentication**: Administrator role required

**Parameters**:


**Response**:


### Create Class Session

Create a new class session.


**Authentication**: Administrator role required

**Parameters**:


**Response**:


🌐 WebSocket APIs {#websockets}
-------------------------------

### Real-time Attendance Updates

Connect to WebSocket for real-time attendance notifications.


**Message Types**:

#### Student Submission


#### AI Validation Result


#### Code Generation


❌ Error Handling
----------------

### Common HTTP Status Codes


### Standard Error Format

All API errors follow this format:


### Common Error Scenarios

#### 1\. CSRF Token Missing


**Solution**: Include X-CSRFToken header

#### 2\. Session Expired


**Solution**: Redirect to login page

#### 3\. Invalid Attendance Code


#### 4\. Permission Denied


### Error Handling Example



📊 API Usage Analytics
----------------------

Based on the SysPonto implementation, here are the most commonly used endpoints:

### High-Traffic Endpoints

1.  **/api/submit-attendance/** - Used by all students during class
    
2.  **/api/generate-code/** - Used by teachers at class start
    
3.  **/api/get-session-submissions/** - Real-time teacher monitoring
    
4.  **/api/validate-attendance/** - Teacher approval actions
    

### Medium-Traffic Endpoints

1.  **/api/student/current-classes/** - Dashboard refreshes
    
2.  **/api/student/today-classes/** - Daily schedule views
    
3.  **/api/run-ai-validation/** - Fraud detection triggers
    
4.  **/api/submit-justification/** - Absence submissions
    

### Low-Traffic Endpoints

1.  **Admin APIs** - User/course management
    
2.  **Analytics APIs** - Reporting and statistics
    
3.  **/api/student/weekly-classes/** - Calendar views
    
4.  **/api/student/attendance-history/** - History reviews
    

🔗 Integration Patterns
-----------------------

### Pattern 1: Student Mobile App


### Pattern 2: Teacher Dashboard Integration



### Pattern 3: LMS Integration


🚀 Performance Optimization
---------------------------

### Caching Strategies


### Database Query Optimization


### API Response Compression


🧪 Testing the API
------------------

### Unit Tests Example


### API Integration Tests


📚 SDK Development
------------------

### Python SDK Template


### JavaScript SDK Template


📖 Additional Resources
-----------------------

### Related Documentation

*   [**Authentication Guide**](authentication.md) - Detailed authentication implementation
    
*   [**User Guide**](../user-guide/index.md) - End-user documentation
    
*   [**WebSocket Integration**](../technical/websockets.md) - Real-time features
    
*   [**Deployment Guide**](../technical/deployment.md) - Production setup
    

### External Resources

*   [**Django REST Framework**](https://www.django-rest-framework.org/) - For future API enhancements
    
*   [**Django Channels**](https://channels.readthedocs.io/) - WebSocket implementation
    
*   [**Postman Collection**](https://documenter.getpostman.com/sysponto) - API testing collection