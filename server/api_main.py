from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import httpx
import uuid
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from database import get_db, User, Interview, init_db
from auth import create_access_token, get_current_user, TokenData, TokenResponse

# Initialize FastAPI app
app = FastAPI(
    title="Nexus Mock Interview API",
    description="Backend API for AI-powered mock interviews",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas
class GoogleAuthRequest(BaseModel):
    id_token: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str]
    picture_url: Optional[str]
    created_at: datetime

class InterviewCreate(BaseModel):
    duration: int
    topic: str
    transcript: str
    score: float
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]

class InterviewResponse(BaseModel):
    id: str
    date: datetime
    duration: int
    topic: str
    score: float
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]

# Startup event
@app.on_event("startup")
async def startup_event():
    init_db()

# Health check endpoint (no database required)
@app.get("/health")
async def health_check():
    from database import db_available
    status_msg = "healthy" if db_available else "running_without_db"
    return {"status": status_msg, "message": "Nexus Mock Interview API"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Nexus Mock Interview API", "status": "running"}

# ==================== AUTH ENDPOINTS ====================

@app.post("/auth/google", response_model=TokenResponse)
async def google_auth(
    auth_request: GoogleAuthRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with Google ID token
    
    Flow:
    1. Flutter app gets ID token from Google Sign-In
    2. App sends token to this endpoint
    3. Server verifies token with Google
    4. Server creates/updates user in database
    5. Server returns JWT for future requests
    """
    try:
        # Verify Google ID token
        idinfo = id_token.verify_oauth2_token(
            auth_request.id_token,
            google_requests.Request(),
            # Note: Add client ID check if needed
        )
        
        # Extract user info from token
        google_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo.get('name')
        picture = idinfo.get('picture')
        
        user = None
        
        if db is not None:
            # Check if user exists
            user = db.query(User).filter(User.google_id == google_id).first()
            
            if user:
                # Update last login
                user.last_login = datetime.utcnow()
                db.commit()
            else:
                # Create new user
                user = User(
                    google_id=google_id,
                    email=email,
                    name=name,
                    picture_url=picture
                )
                db.add(user)
                db.commit()
                db.refresh(user)
        else:
            # Mock user for no-db mode
            user = type('User', (), {
                'id': uuid.uuid4(),
                'email': email,
                'name': name,
                'picture_url': picture
            })()
        
        # Create JWT token
        token = create_access_token({
            "user_id": str(user.id),
            "email": user.email
        })
        
        return TokenResponse(
            access_token=token,
            user={
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
                "picture_url": user.picture_url
            }
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {str(e)}"
        )
    except Exception as e:
        # Log error
        print(f"Auth Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current authenticated user's information"""
    if db is None:
         # Return mock info from token data
         return UserResponse(
            id=current_user.user_id,
            email=current_user.email,
            name="Test User (No DB)",
            picture_url=None,
            created_at=datetime.utcnow()
        )

    user = db.query(User).filter(User.id == current_user.user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        picture_url=user.picture_url,
        created_at=user.created_at
    )

# ==================== INTERVIEW ENDPOINTS ====================

@app.post("/api/interviews", response_model=InterviewResponse)
@app.post("/api/interviews", response_model=InterviewResponse)
async def create_interview(
    interview: InterviewCreate,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save interview results"""
    if db is None:
        # Mock response for no-db mode
        return InterviewResponse(
            id=str(uuid.uuid4()),
            date=datetime.utcnow(),
            duration=interview.duration,
            topic=interview.topic,
            score=interview.score,
            strengths=interview.strengths,
            weaknesses=interview.weaknesses,
            suggestions=interview.suggestions
        )

    new_interview = Interview(
        user_id=current_user.user_id,
        duration=interview.duration,
        topic=interview.topic,
        transcript=interview.transcript,
        score=interview.score,
        strengths=interview.strengths,
        weaknesses=interview.weaknesses,
        suggestions=interview.suggestions
    )
    
    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)
    
    return InterviewResponse(
        id=str(new_interview.id),
        date=new_interview.date,
        duration=new_interview.duration,
        topic=new_interview.topic,
        score=new_interview.score,
        strengths=new_interview.strengths,
        weaknesses=new_interview.weaknesses,
        suggestions=new_interview.suggestions
    )

@app.get("/api/interviews", response_model=List[InterviewResponse])
async def get_user_interviews(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    """Get user's interview history"""
    if db is None:
        return []

    interviews = db.query(Interview)\
        .filter(Interview.user_id == current_user.user_id)\
        .order_by(Interview.date.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()
    
    return [
        InterviewResponse(
            id=str(i.id),
            date=i.date,
            duration=i.duration,
            topic=i.topic,
            score=i.score,
            strengths=i.strengths,
            weaknesses=i.weaknesses,
            suggestions=i.suggestions
        )
        for i in interviews
    ]

@app.get("/api/interviews/{interview_id}", response_model=InterviewResponse)
async def get_interview(
    interview_id: str,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific interview details"""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found (DB unavailable)"
        )

    interview = db.query(Interview)\
        .filter(
            Interview.id == interview_id,
            Interview.user_id == current_user.user_id
        )\
        .first()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    return InterviewResponse(
        id=str(interview.id),
        date=interview.date,
        duration=interview.duration,
        topic=interview.topic,
        score=interview.score,
        strengths=interview.strengths,
        weaknesses=interview.weaknesses,
        suggestions=interview.suggestions
    )

@app.get("/api/stats")
async def get_user_stats(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user statistics"""
    if db is None:
        return {
            "total_interviews": 0,
            "average_score": 0,
            "last_interview": None
        }

    from sqlalchemy import func
    
    stats = db.query(
        func.count(Interview.id).label('total_interviews'),
        func.avg(Interview.score).label('average_score'),
        func.max(Interview.date).label('last_interview')
    ).filter(Interview.user_id == current_user.user_id).first()
    
    return {
        "total_interviews": stats.total_interviews or 0,
        "average_score": round(stats.average_score, 2) if stats.average_score else 0,
        "last_interview": stats.last_interview
    }

# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
