from fastapi import Depends

from app.api.deps import get_current_user, get_current_workspace, get_db

DB_DEP = Depends(get_db)
USER_DEP = Depends(get_current_user)
WORKSPACE_DEP = Depends(get_current_workspace)

PROJECT_NOT_FOUND = "Project not found"
