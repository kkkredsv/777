"""
Admin Handlers Module
Created: 2026-01-08 13:42:31 UTC
Author: kkkredsv

This module provides admin panel functionality and handlers for administrative operations.
"""

from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum


class AdminRole(Enum):
    """Admin role levels"""
    SUPER_ADMIN = 3
    ADMIN = 2
    MODERATOR = 1


class AdminPanel:
    """Main admin panel class for managing administrative operations"""
    
    def __init__(self):
        """Initialize the admin panel"""
        self.admins: Dict[int, Dict[str, Any]] = {}
        self.created_at = datetime.utcnow()
        self.logs: List[str] = []
    
    def add_admin(self, admin_id: int, username: str, role: AdminRole) -> bool:
        """
        Add a new admin user
        
        Args:
            admin_id: Unique admin identifier
            username: Admin username
            role: Admin role level
            
        Returns:
            bool: True if admin was added successfully
        """
        if admin_id in self.admins:
            self._log(f"Admin {admin_id} already exists")
            return False
        
        self.admins[admin_id] = {
            "username": username,
            "role": role,
            "created_at": datetime.utcnow(),
            "last_action": None
        }
        self._log(f"Admin {username} (ID: {admin_id}) added with role {role.name}")
        return True
    
    def remove_admin(self, admin_id: int) -> bool:
        """
        Remove an admin user
        
        Args:
            admin_id: Admin identifier to remove
            
        Returns:
            bool: True if admin was removed successfully
        """
        if admin_id not in self.admins:
            self._log(f"Admin {admin_id} not found")
            return False
        
        username = self.admins[admin_id]["username"]
        del self.admins[admin_id]
        self._log(f"Admin {username} (ID: {admin_id}) removed")
        return True
    
    def get_admin(self, admin_id: int) -> Optional[Dict[str, Any]]:
        """
        Get admin information
        
        Args:
            admin_id: Admin identifier
            
        Returns:
            Dict containing admin information or None if not found
        """
        return self.admins.get(admin_id)
    
    def get_all_admins(self) -> Dict[int, Dict[str, Any]]:
        """
        Get all admin users
        
        Returns:
            Dictionary of all admins
        """
        return self.admins.copy()
    
    def update_admin_role(self, admin_id: int, new_role: AdminRole) -> bool:
        """
        Update an admin's role level
        
        Args:
            admin_id: Admin identifier
            new_role: New role to assign
            
        Returns:
            bool: True if role was updated successfully
        """
        if admin_id not in self.admins:
            self._log(f"Admin {admin_id} not found")
            return False
        
        old_role = self.admins[admin_id]["role"].name
        self.admins[admin_id]["role"] = new_role
        self._log(f"Admin {admin_id} role updated from {old_role} to {new_role.name}")
        return True
    
    def record_action(self, admin_id: int, action: str) -> bool:
        """
        Record an admin action
        
        Args:
            admin_id: Admin identifier
            action: Description of the action performed
            
        Returns:
            bool: True if action was recorded successfully
        """
        if admin_id not in self.admins:
            self._log(f"Admin {admin_id} not found")
            return False
        
        self.admins[admin_id]["last_action"] = {
            "action": action,
            "timestamp": datetime.utcnow()
        }
        self._log(f"Action recorded for admin {admin_id}: {action}")
        return True
    
    def get_logs(self, limit: Optional[int] = None) -> List[str]:
        """
        Get admin panel logs
        
        Args:
            limit: Maximum number of logs to return (None for all)
            
        Returns:
            List of log entries
        """
        if limit:
            return self.logs[-limit:]
        return self.logs.copy()
    
    def clear_logs(self) -> None:
        """Clear all admin panel logs"""
        self.logs.clear()
        self._log("Logs cleared")
    
    def _log(self, message: str) -> None:
        """
        Internal logging method
        
        Args:
            message: Log message
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get admin panel statistics
        
        Returns:
            Dictionary containing panel statistics
        """
        role_counts = {role.name: 0 for role in AdminRole}
        for admin in self.admins.values():
            role_counts[admin["role"].name] += 1
        
        return {
            "total_admins": len(self.admins),
            "role_counts": role_counts,
            "panel_created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "total_logs": len(self.logs)
        }


class AdminHandlers:
    """Handler class for admin operations"""
    
    def __init__(self):
        """Initialize admin handlers"""
        self.panel = AdminPanel()
    
    def handle_admin_creation(self, admin_id: int, username: str, role: str) -> Dict[str, Any]:
        """
        Handle admin user creation
        
        Args:
            admin_id: Admin identifier
            username: Admin username
            role: Role name (SUPER_ADMIN, ADMIN, MODERATOR)
            
        Returns:
            Response dictionary
        """
        try:
            role_enum = AdminRole[role.upper()]
            success = self.panel.add_admin(admin_id, username, role_enum)
            
            return {
                "success": success,
                "message": f"Admin {username} created successfully" if success else "Admin already exists",
                "admin_id": admin_id
            }
        except KeyError:
            return {
                "success": False,
                "message": f"Invalid role: {role}",
                "admin_id": admin_id
            }
    
    def handle_admin_deletion(self, admin_id: int) -> Dict[str, Any]:
        """
        Handle admin user deletion
        
        Args:
            admin_id: Admin identifier to delete
            
        Returns:
            Response dictionary
        """
        success = self.panel.remove_admin(admin_id)
        return {
            "success": success,
            "message": "Admin deleted successfully" if success else "Admin not found",
            "admin_id": admin_id
        }
    
    def handle_role_update(self, admin_id: int, new_role: str) -> Dict[str, Any]:
        """
        Handle admin role update
        
        Args:
            admin_id: Admin identifier
            new_role: New role name
            
        Returns:
            Response dictionary
        """
        try:
            role_enum = AdminRole[new_role.upper()]
            success = self.panel.update_admin_role(admin_id, role_enum)
            
            return {
                "success": success,
                "message": f"Role updated to {new_role}" if success else "Admin not found",
                "admin_id": admin_id,
                "new_role": new_role
            }
        except KeyError:
            return {
                "success": False,
                "message": f"Invalid role: {new_role}",
                "admin_id": admin_id
            }
    
    def handle_action_logging(self, admin_id: int, action: str) -> Dict[str, Any]:
        """
        Handle action logging
        
        Args:
            admin_id: Admin identifier
            action: Action description
            
        Returns:
            Response dictionary
        """
        success = self.panel.record_action(admin_id, action)
        return {
            "success": success,
            "message": "Action logged successfully" if success else "Admin not found",
            "admin_id": admin_id
        }
    
    def handle_get_panel_stats(self) -> Dict[str, Any]:
        """
        Handle statistics request
        
        Returns:
            Panel statistics
        """
        return self.panel.get_stats()
    
    def handle_get_logs(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Handle logs request
        
        Args:
            limit: Maximum number of logs to return
            
        Returns:
            Response dictionary with logs
        """
        logs = self.panel.get_logs(limit)
        return {
            "success": True,
            "logs": logs,
            "total_logs": len(logs)
        }


# Global admin handlers instance
admin_handlers = AdminHandlers()
