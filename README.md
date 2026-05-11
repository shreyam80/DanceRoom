# DanceRoom MVP

## Structure
- `frontend/`: React + Vite + TypeScript + Tailwind
- `backend/`: FastAPI + Supabase service role integration
- `supabase/`: SQL migrations

## Prerequisites
1. Create Supabase project.
2. Run `supabase/migrations/001_init.sql` in SQL editor.
3. Create storage bucket named `videos` (public for MVP).
4. Copy `.env.example` to `.env` and fill values.

## Run backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Run frontend
```bash
cd frontend
npm install
npm run dev
```

## MVP flows
- Signup/login with role (`choreographer` or `dancer`).
- Choreographer creates org/team/routine and uploads video to Supabase Storage.
- Choreographer adds timestamped comments with targets.
- Target expansion writes `comment_recipients` rows.
- Dancer playback auto-pauses once per unacknowledged comment and persists acknowledgement.
- Both roles can resolve comments.
