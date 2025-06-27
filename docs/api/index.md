API Reference
=============

The SysPonto API provides programmatic access to the attendance management system. This RESTful API enables integration with external systems, mobile applications, and custom interfaces.

🌟 API Features
---------------

*   **Role-based Access Control** - Different endpoints for students, teachers, and administrators
    
*   **Real-time Updates** - WebSocket connections for live attendance monitoring
    
*   **Secure Authentication** - Django session-based authentication with CSRF protection
    
*   **Data Validation** - Comprehensive input validation and error handling
    
*   **Mobile Optimized** - Designed for mobile app integration
    

📊 API Statistics
-----------------

Based on the current SysPonto implementation:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   ResourceEndpointsMethodsAuthentication RequiredAttendance6GET, POSTYesUsers4GET, POST, PUT, DELETEAdmin onlyCourses4GET, POST, PUT, DELETETeacher/AdminSessions3GET, POST, DELETETeacher/AdminAnalytics5GETRole-based   `

🔗 Base URLs
------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   Production: https://your-domain.com/  Development: http://localhost:8000/  API Prefix: /api/ (for dedicated API endpoints)   `

🔐 Authentication Methods
-------------------------

SysPonto uses Django's built-in authentication system:

1.  **Session Authentication** - Web browser sessions
    
2.  **CSRF Protection** - Required for all state-changing operations
    
3.  **Role-based Permissions** - Student, Teacher, Administrator roles
    

📱 Supported Clients
--------------------

*   **Web Browsers** - Full featured web interface
    
*   **Mobile Apps** - Responsive design with API access
    
*   **Third-party Systems** - Integration via API endpoints
    
*   **LMS Integration** - Learning Management System connectivity
    

🚀 Quick Start
--------------

### 1\. Authentication

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Login to get session  curl -X POST http://localhost:8000/login/ \    -d "username=your_username&password=your_password" \    -c cookies.txt   `

### 2\. Generate Attendance Code (Teacher)

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Generate code for class session  curl -X POST http://localhost:8000/api/generate-code/ \    -b cookies.txt \    -d "class_session_id=123" \    -H "X-CSRFToken: your_csrf_token"   `

### 3\. Submit Attendance (Student)

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Submit attendance code  curl -X POST http://localhost:8000/api/submit-attendance/ \    -b cookies.txt \    -d "attendance_code=ABC123&simulated_latitude=41.5369&simulated_longitude=-8.4239" \    -H "X-CSRFToken: your_csrf_token"   `

📋 Response Format
------------------

All API responses follow this standard format:

### Success Response

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "success",      "message": "Operation completed successfully",      "data": {          // Response data here      }  }   `

### Error Response

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   json{      "status": "error",      "message": "Error description",      "errors": {          "field": ["Error details"]      }  }   `

🔧 Rate Limiting
----------------

Current rate limits (can be configured):

*   **Authentication**: 5 requests per minute
    
*   **Code Generation**: 10 requests per minute
    
*   **Data Retrieval**: 100 requests per minute
    
*   **WebSocket Connections**: 5 concurrent per user
    

📖 API Categories
-----------------

### [Authentication APIs](authentication.md)

*   Login/Logout
    
*   Session Management
    
*   CSRF Token Handling
    
*   Role Verification
    

### [Attendance APIs](endpoints.md#attendance)

*   Generate Attendance Codes
    
*   Submit Attendance
    
*   Validate Attendance
    
*   AI Fraud Detection
    
*   Bulk Validation
    

### [User Management APIs](endpoints.md#users)

*   Create Users
    
*   Update User Details
    
*   Role Management
    
*   User Deletion
    

### [Course Management APIs](endpoints.md#courses)

*   Course Creation
    
*   Teacher Assignment
    
*   Session Scheduling
    
*   Enrollment Management
    

### [Analytics APIs](endpoints.md#analytics)

*   Attendance Statistics
    
*   Student Performance
    
*   Course Analytics
    
*   System Metrics
    

### [Real-time APIs](endpoints.md#websockets)

*   WebSocket Connections
    
*   Live Notifications
    
*   Real-time Updates
    

🛠 Integration Examples
-----------------------

### Python Integration

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pythonimport requests  class SysPontoAPI:      def __init__(self, base_url):          self.base_url = base_url          self.session = requests.Session()      def login(self, username, password):          response = self.session.post(              f"{self.base_url}/login/",              data={"username": username, "password": password}          )          return response.status_code == 200      def generate_code(self, session_id):          csrf_token = self.session.cookies.get('csrftoken')          response = self.session.post(              f"{self.base_url}/api/generate-code/",              data={"class_session_id": session_id},              headers={"X-CSRFToken": csrf_token}          )          return response.json()   `

### JavaScript Integration

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   javascriptclass SysPontoAPI {      constructor(baseUrl) {          this.baseUrl = baseUrl;      }      async submitAttendance(code, latitude, longitude) {          const csrfToken = this.getCSRFToken();          const response = await fetch(`${this.baseUrl}/api/submit-attendance/`, {              method: 'POST',              headers: {                  'Content-Type': 'application/x-www-form-urlencoded',                  'X-CSRFToken': csrfToken              },              body: new URLSearchParams({                  attendance_code: code,                  simulated_latitude: latitude,                  simulated_longitude: longitude              })          });          return response.json();      }      getCSRFToken() {          return document.querySelector('[name=csrfmiddlewaretoken]').value;      }  }   ``


🆘 Support
----------

*   **API Documentation Issues**: [GitHub Issues](https://github.com/pedrox86lopes/sysponto/issues)
    
    
*   **Technical Support**: Available during business hours
    

docs/api/authentication.md - Authentication Guide
=================================================

Authentication
==============

SysPonto uses Django's built-in authentication system with session-based authentication and CSRF protection for web security.

🔐 Authentication Flow
----------------------

### 1\. Login Process

#### Web Login


**Success Response (302 Redirect):**


**Error Response (200 with form errors):**


#### API Login Check


**Response:**


### 2\. Session Management

Django automatically manages sessions via cookies:

*   **Session Cookie**: sessionid - Contains encrypted session data
    
*   **CSRF Cookie**: csrftoken - Protection against cross-site request forgery
    
*   **Session Expiry**: Configurable (default: 2 weeks for "Remember Me")
    

### 3\. CSRF Protection

All state-changing requests require CSRF token:

#### Getting CSRF Token


#### Using CSRF Token


👥 Role-Based Access Control
----------------------------

### User Roles

SysPonto implements three main roles:

#### 1\. Student Role


#### 2\. Teacher Role


#### 3\. Administrator Role


### Permission Decorators

The API uses Django decorators for access control:


🔧 Implementation Examples
--------------------------

### Python Requests Session


### JavaScript Fetch API


### cURL Examples

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bash# Login and save cookies  curl -X POST http://localhost:8000/login/ \    -d "username=prof.silva&password=password123" \    -c cookies.txt \    -b cookies.txt  # Extract CSRF token from cookies  CSRF_TOKEN=$(grep csrftoken cookies.txt | cut -f7)  # Make authenticated API request  curl -X POST http://localhost:8000/api/generate-code/ \    -b cookies.txt \    -H "X-CSRFToken: $CSRF_TOKEN" \    -d "class_session_id=1"   `

🚨 Security Considerations
--------------------------

### Best Practices

1.  python# settings.pySECURE\_SSL\_REDIRECT = TrueSESSION\_COOKIE\_SECURE = TrueCSRF\_COOKIE\_SECURE = True
    
2.  javascriptasync function apiRequest(endpoint, data) { const response = await fetch(endpoint, { method: 'POST', body: data, credentials: 'include' }); if (response.status === 403) { // Session expired, redirect to login window.location.href = '/login/'; return; } return response.json();}
    
3.  javascript// Check user role before showing UI elementsif (user.role === 'teacher') { showTeacherControls();} else if (user.role === 'student') { showStudentControls();}
    

### Common Authentication Errors

#### 1\. Missing CSRF Token (403 Forbidden)


**Solution**: Include X-CSRFToken header in requests

#### 2\. Session Expired (401 Unauthorized)


**Solution**: Redirect user to login page

#### 3\. Insufficient Permissions (403 Forbidden)


**Solution**: Check user role and permissions

🔄 Session Management
---------------------

### Extending Session Lifetime


### Logout Implementation


**Response:**


📱 Mobile App Integration
-------------------------

For mobile applications, consider implementing token-based authentication alongside session authentication:
Not yet

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

Get classes currently running for the student.

**Authentication**: Student role required

**Response**:


### Get Today's Classes

Get all classes scheduled for today.


**Authentication**: Student role required

**Response**:


### Get Weekly Classes

Get all classes for the current week.


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

Create a new user account.


**Authentication**: Administrator role required

**Parameters**:


**Response**:


### Create Course

Create a new course.


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