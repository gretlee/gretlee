from functools import wraps
from flask import request, jsonify

# Define role permissions
ROLES = {
    'admin': {
        'permissions': [
            'create_report',
            'view_reports',
            'manage_centers',
            'run_optimization',
            'view_predictions',
            'view_analytics',
            'manage_users'
        ],
        'description': 'Full system access - can manage centers, run optimization, and view predictions'
    },
    'relief_worker': {
        'permissions': [
            'create_report',
            'view_reports'
        ],
        'description': 'Can submit and view disaster reports'
    }
}

def get_role_permissions(role):
    """
    Get permissions for a given role.
    
    Args:
        role: Role name (admin or relief_worker)
    
    Returns:
        List of permissions for the role
    """
    return ROLES.get(role, {}).get('permissions', [])

def has_permission(role, permission):
    """
    Check if a role has a specific permission.
    
    Args:
        role: Role name
        permission: Permission to check
    
    Returns:
        Boolean indicating if role has permission
    """
    role_permissions = get_role_permissions(role)
    return permission in role_permissions

def require_permission(permission):
    """
    Decorator to require a specific permission for a route.
    
    Usage:
        @app.route('/admin')
        @require_permission('manage_centers')
        def admin_route():
            return "Admin content"
    
    Args:
        permission: Permission required to access the route
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get role from request headers (in production, use proper JWT/session auth)
            role = request.headers.get('X-User-Role', 'relief_worker')
            
            if not has_permission(role, permission):
                return jsonify({
                    'success': False,
                    'error': f'Permission denied. Required permission: {permission}',
                    'role': role
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_role(required_role):
    """
    Decorator to require a specific role for a route.
    
    Usage:
        @app.route('/admin')
        @require_role('admin')
        def admin_route():
            return "Admin content"
    
    Args:
        required_role: Role required to access the route
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get role from request headers
            role = request.headers.get('X-User-Role', 'relief_worker')
            
            if role != required_role:
                return jsonify({
                    'success': False,
                    'error': f'Access denied. Required role: {required_role}',
                    'current_role': role
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_role(role):
    """
    Validate if a role exists.
    
    Args:
        role: Role name to validate
    
    Returns:
        Boolean indicating if role is valid
    """
    return role in ROLES

def get_all_roles():
    """
    Get all available roles with their descriptions.
    
    Returns:
        Dictionary of roles with descriptions
    """
    return {
        role: {
            'description': info['description'],
            'permissions': info['permissions']
        }
        for role, info in ROLES.items()
    }
