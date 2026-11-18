# Telo

A web app that lets customers get their body measurements from photos, with no account needed, and share them with a tailor near them. Tailors log in to view and confirm the measurements, then create a contract that sets when the cloth will be ready.



## The Problem

Taking body measurements for tailored clothes usually needs a visit to the tailor. This project lets the customer capture measurements from home using their phone, and lets the tailor review them before starting work.

## How It Works

- **Customers have no account.** They enter basic details, take photos, and pick a tailor.
- **Vendor tailors have accounts.** They log in to view the measurements of the customers assigned to them.
- **Location matching.** Customers are shown tailors located near them.
- **Contract.** The tailor creates a contract with the date the cloth will be ready and the collection date, with a one-week gap for collection.
- **Tailor confirmation.** AI measurements are estimates. The tailor can edit and confirm every value.

---

## MVP Scope

### Customer flow

1. Open the page (no signup) and enter name, phone number, height and location.
2. See nearby tailors sorted by distance and choose one.
3. Take a front photo and a side photo using a guided camera screen.
4. The AI estimates the measurements.
5. Measurements are saved and linked to the chosen tailor.
6. Open a link (no account) to view the contract status.

### Tailor flow

1. Log in.
2. See the list of assigned customers and their measurements.
3. Edit and confirm the measurements.
4. Create a contract with the ready date and collection date.

### Measurements captured

Shoulder, chest, waist, hip, sleeve and inseam.

### Not in the MVP

- Customer accounts
- 3D body scanning (SMPL / PyTorch)
- Payments
- Chat
- Notifications beyond an SMS or WhatsApp link
- Mobile apps (the web app is mobile-friendly)

---

## AI Measurement Approach

The goal is to make capture conditions consistent, so results do not depend on how good the phone camera is.

1. **Guided capture.** A body outline on the camera screen. The shutter is enabled only when head, hands and feet are visible and the body is upright.
2. **Phone orientation check.** The phone must be held vertically.
3. **Timer.** A 10-second timer so the phone can be propped up 2 to 3 metres away.
4. **Quality checks.** Reject photos that are blurry, too dark or too bright, too small in the frame, or cropped.
5. **Scale.** The customer's height converts pixels to centimetres. An optional reference object (A4 sheet or bank card) improves accuracy.
6. **Burst capture.** Capture 10 to 20 frames and take the median of each measurement to reduce noise.
7. **Pose and segmentation.** MediaPipe Pose gives body landmarks for widths and lengths. The segmentation mask gives body width (front) and depth (side) for chest, waist and hip circumferences, estimated as an ellipse.
8. **Tailor correction.** The AI estimate and the tailor-confirmed value are both stored. Later, a simple regression (scikit-learn) learns the usual error and corrects it.

Expected accuracy is roughly 2 to 4 cm on most measurements. This is why tailor confirmation is part of the MVP.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite), Tailwind CSS, MediaPipe Tasks Vision (JS), Leaflet + OpenStreetMap, Axios |
| Backend | Django, Django REST Framework, SimpleJWT (tailors only) |
| Background jobs | Celery + Redis |
| Database | PostgreSQL (PostGIS later for nearest-tailor queries) |
| AI / CV | MediaPipe Pose (Python), OpenCV, NumPy, scikit-learn |
| Storage | Cloudinary or AWS S3 |
| Messaging | Termii or Twilio / WhatsApp Business API |
| Deployment | Docker, on a small VPS or Render / Railway |

### Why not SMPL / PyTorch for the MVP

It needs a GPU, the SMPL license restricts commercial use without a paid license, setup is heavy, and it still cannot see through loose clothing. Revisit it once there is enough AI-versus-tailor data to show MediaPipe is not accurate enough.

---

## Data Models

- **Tailor**: linked to the Vendor, with latitude and longitude.
- **Customer**: name, phone, email. No user account.
- **MeasurementSession**: customer, tailor, photos, height, status.
- **Measurement**: individual values, with AI-estimated and tailor-confirmed versions.
- **Contract**: tailor, customer, ready date, collection date, status.

Nearby tailors are found with a Haversine distance calculation on the stored coordinates.

---

## Project Structure

```
ai-measurement/
├── backend/
│   ├── config/              # settings, urls, celery.py
│   ├── apps/
│   │   ├── tailors/         # Tailor profile, location
│   │   ├── customers/       # Customer (no user account)
│   │   ├── measurements/    # sessions, photos, values
│   │   │   └── ml/          # pose.py, quality.py, scale.py, estimate.py
│   │   └── contracts/       # contract, ready/collection dates
│   ├── manage.py
│   └── requirements.txt
├── frontend/                # React (Vite)
├── docker-compose.yml       # postgres + redis
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10 to 3.12 (MediaPipe is picky about versions)
- Node.js 18+
- Docker (for PostgreSQL and Redis)

### 1. Start PostgreSQL and Redis

```bash
docker compose up -d
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

In a second terminal, start the Celery worker:

```bash
cd backend
source venv/bin/activate
celery -A config worker -l info
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin
- Frontend: http://localhost:5173

### Environment variables

Create `backend/.env` (and keep it out of Git):

```
SECRET_KEY=change-me
DEBUG=True
DATABASE_URL=postgres://measure:measure@localhost:5432/measure
CELERY_BROKER_URL=redis://localhost:6379/0
```

---

## Build Order

1. Django models
2. The `ml/` module, tested on sample photos from the command line before any API exists
3. Upload endpoint plus Celery task
4. Tailor login and dashboard
5. Customer capture flow in React
6. Customer contract link (signed, expiring URL)

The measuring step carries the most risk, so it is built and tested first.

---

## Privacy

Photos of people's bodies are sensitive. The MVP should include:

- A consent screen before any photo is taken
- Deleting raw photos shortly after processing
- Photo and measurement access limited to the assigned tailor
- Signed, expiring links for customers instead of accounts

---

## Roadmap

- [ ] Models and migrations
- [ ] Pose and quality-check module
- [ ] Measurement API
- [ ] Tailor dashboard
- [ ] Customer capture flow
- [ ] Contracts and customer link
- [ ] SMS / WhatsApp notifications
- [ ] Correction model trained on tailor edits
- [ ] Evaluate 3D body-model approach once enough data exists