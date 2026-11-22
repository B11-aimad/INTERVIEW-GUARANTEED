
# 🚀 Entretien Garanti

> **AI-powered career & job application management platform**  
> **Human-in-the-Loop · Explainable AI · CV-Grounded Generation · Automatic Stop Rule**

**Entretien Garanti** est une plateforme intelligente de gestion de recherche d'emploi et de candidatures basée sur l'intelligence artificielle.

L'objectif du projet est d'automatiser les tâches répétitives liées à la recherche d'emploi tout en conservant un **contrôle humain obligatoire** sur les informations du candidat et les décisions importantes.

La plateforme permet notamment de :

- 📄 analyser et structurer automatiquement un CV ;
- 👤 construire un profil candidat exploitable par l'IA ;
- 🔎 collecter et normaliser des offres d'emploi ;
- 🎯 calculer un score de matching explicable ;
- 📊 classer les offres selon leur pertinence ;
- ✍️ générer des lettres de motivation personnalisées ;
- 🛡️ empêcher l'IA d'inventer des compétences ou expériences ;
- 📋 gérer et suivre les candidatures ;
- 📈 fournir un tableau de bord de recherche d'emploi ;
- 🛑 arrêter automatiquement l'agent lorsqu'un entretien est obtenu ;
- 🔐 gérer le consentement, la confidentialité et la suppression des données.

---

## 📌 Table of Contents

- [Présentation](#-présentation)
- [Objectifs](#-objectifs)
- [Fonctionnalités](#-fonctionnalités)
- [Principes métier](#-principes-métier)
- [Matching Score](#-matching-score)
- [AI & Anti-Hallucination](#-ai--anti-hallucination)
- [Automatic Stop Rule](#-automatic-stop-rule)
- [Subscription Plans](#-subscription-plans)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Application Workflow](#-application-workflow)
- [Data Model](#-data-model)
- [Backend](#-backend)
- [Frontend](#-frontend)
- [Database](#-database)
- [Security & Privacy](#-security--privacy)
- [Docker](#-docker)
- [Configuration](#-configuration)
- [Development](#-development)
- [Testing](#-testing)
- [API Overview](#-api-overview)
- [Development Roadmap](#-development-roadmap)
- [Project Status](#-project-status)
- [Future Improvements](#-future-improvements)
- [License](#-license)

---

# 🎯 Présentation

La recherche d'emploi implique généralement plusieurs tâches répétitives :

1. rechercher des offres sur différentes plateformes ;
2. comparer chaque offre avec son profil ;
3. identifier les compétences demandées ;
4. adapter son CV ;
5. rédiger une lettre de motivation ;
6. envoyer la candidature ;
7. suivre les réponses ;
8. répéter le processus pour chaque nouvelle offre.

**Entretien Garanti** cherche à centraliser et automatiser cette chaîne de travail.

L'architecture repose sur une approche **Human-in-the-Loop** : l'intelligence artificielle automatise les tâches d'analyse, de recommandation et de génération, mais le candidat conserve le contrôle sur ses informations et la validation des candidatures.

---

# 🎯 Objectifs

## Objectif principal

Construire un agent IA capable d'assister le candidat dans l'ensemble du processus de recherche d'emploi :

```text
CV
 │
 ▼
Analyse du profil
 │
 ▼
Recherche d'offres
 │
 ▼
Matching
 │
 ▼
Classement
 │
 ▼
Génération de candidature
 │
 ▼
Validation humaine
 │
 ▼
Candidature
 │
 ▼
Suivi
 │
 ▼
Entretien obtenu
 │
 ▼
🛑 AGENT ARRÊTÉ
```

## Objectifs fonctionnels

- Automatiser l'analyse du CV.
- Structurer les informations professionnelles.
- Rechercher des offres pertinentes.
- Calculer un score de compatibilité.
- Expliquer les résultats du matching.
- Générer des lettres personnalisées.
- Éviter les hallucinations de l'IA.
- Gérer les candidatures.
- Suivre leur statut.
- Respecter les quotas des formules.
- Arrêter automatiquement l'agent lorsqu'un entretien est obtenu.

---

# ✨ Fonctionnalités

## 👤 Gestion du candidat

- Création de compte
- Authentification JWT
- Gestion du profil
- Gestion des préférences professionnelles
- Gestion des compétences
- Gestion des expériences
- Gestion des formations
- Gestion des langues

---

## 📄 CV Parsing

Le candidat peut importer son CV afin de permettre au système d'en extraire automatiquement les informations utiles.

### Formats ciblés

```text
PDF
DOCX
```

### Informations extraites

```text
Profil
├── Informations personnelles
├── Poste recherché
├── Compétences
├── Expériences professionnelles
├── Formations
├── Langues
└── Préférences
```

### Human-in-the-Loop

Les informations extraites automatiquement doivent être :

```text
CV
 ↓
Extraction automatique
 ↓
Profil proposé
 ↓
👤 Validation humaine
 ↓
Profil validé
```

Le profil validé constitue ensuite la **source de vérité** utilisée par les composants IA.

---

# 🔎 Recherche et gestion des offres

La plateforme est conçue pour récupérer des offres provenant de plusieurs sources.

Les données provenant des différentes sources sont transformées vers un format commun.

### Exemple de structure normalisée

```text
JobOffer
├── id
├── source
├── title
├── company
├── location
├── description
├── requirements
├── employment_type
├── url
└── publication_date
```

La normalisation permet au moteur de matching de travailler indépendamment de la source d'origine.

---

# 🎯 Explainable Matching

Le moteur de matching utilise un score pondéré sur trois dimensions principales.

## Formule

```text
Matching Score =
    45% × Semantic Similarity
  + 35% × Skills Alignment
  + 20% × Preferences Alignment
```

### 1. 🧠 Semantic Similarity — 45%

Mesure la proximité sémantique entre :

```text
Candidate Profile
        ↕
Job Description
```

Cette composante peut être implémentée à l'aide de représentations textuelles telles que :

- TF-IDF ;
- embeddings ;
- similarité cosinus.

---

### 2. 🛠️ Skills Alignment — 35%

Compare les compétences du candidat avec les compétences et exigences identifiées dans l'offre.

Exemple :

```text
Candidate Skills:
Python
Machine Learning
SQL
Docker
FastAPI

Job Requirements:
Python
Machine Learning
SQL
Docker
AWS
```

Le système peut alors identifier :

```text
Matched:
✓ Python
✓ Machine Learning
✓ SQL
✓ Docker

Missing:
○ AWS
```

---

### 3. 📍 Preferences Alignment — 20%

Cette partie prend en compte les préférences validées du candidat, par exemple :

- localisation ;
- type de contrat ;
- poste recherché ;
- autres critères configurés dans le profil.

---

## Exemple de résultat

```text
┌─────────────────────────────────────────┐
│ Backend AI Engineer                     │
│                                         │
│ Matching Score: 87%                     │
│                                         │
│ Semantic Similarity       91%           │
│ Skills Alignment          86%           │
│ Preferences Alignment     82%           │
│                                         │
│ ✓ Python                  Matched        │
│ ✓ Machine Learning        Matched        │
│ ✓ FastAPI                 Matched        │
│ ✓ Docker                  Matched        │
│ ○ AWS                     Missing        │
└─────────────────────────────────────────┘
```

Le score doit être accompagné d'une **explication compréhensible** plutôt que présenté comme une décision opaque.

---

# 🤖 AI & Anti-Hallucination

L'un des principes fondamentaux du projet est que l'IA ne doit pas inventer d'informations concernant le candidat.

## Source de vérité

```text
CV
 ↓
Extraction
 ↓
Human Validation
 ↓
Validated Candidate Profile
 ↓
AI Generation
```

Le LLM ne doit utiliser que les informations présentes dans le profil validé.

### Interdiction

L'IA ne doit pas inventer :

- ❌ une expérience professionnelle ;
- ❌ une compétence ;
- ❌ un diplôme ;
- ❌ une certification ;
- ❌ une entreprise ;
- ❌ un projet ;
- ❌ une responsabilité ;
- ❌ une technologie jamais utilisée par le candidat.

### Exemple

Si le profil contient :

```text
Python
SQL
Machine Learning
Docker
```

Le système ne doit jamais générer :

```text
AWS Expert
Kubernetes Expert
10 years of experience
Certified AWS Solutions Architect
```

si ces informations ne sont pas présentes dans les données validées.

---

# ✍️ CV-Grounded Cover Letter Generation

La génération de lettre suit le pipeline suivant :

```text
Validated Candidate Profile
          +
      Job Offer
          │
          ▼
   Context Builder
          │
          ▼
     LLM Service
          │
          ▼
Generated Cover Letter
          │
          ▼
Validation / Review
          │
          ▼
Candidate
```

Le contexte envoyé au modèle doit être contrôlé afin de limiter les hallucinations.

La lettre doit être :

- personnalisée ;
- cohérente avec le CV ;
- adaptée à l'offre ;
- professionnelle ;
- fidèle aux informations validées.

---

# 🛑 Automatic Stop Rule

L'agent possède deux états principaux :

```text
ACTIF
ARRETE
```

## État initial

```text
ACTIF
```

L'agent peut effectuer les opérations autorisées par la formule du candidat.

---

## Obtention d'un entretien

Lorsqu'un entretien est enregistré :

```text
Interview Obtained
       │
       ▼
Stop Rule
       │
       ▼
Agent = ARRETE
       │
       ▼
New Applications Blocked
```

### Règle métier

```text
IF application.status == "INTERVIEW_OBTAINED"
THEN
    agent.status = "ARRETE"
    block_new_applications = true
```

Cette règle permet d'éviter que l'agent continue automatiquement à envoyer des candidatures alors que l'objectif principal — obtenir un entretien — est atteint.

---

# 💳 Subscription Plans

Le projet prévoit trois formules simulées :

| Plan | Positionnement | Gestion des quotas |
|---|---|---|
| 🟢 Découverte | Découverte de la plateforme | Limitée |
| 🔵 Accélérateur | Recherche active | Intermédiaire |
| 🟣 Garanti | Automatisation avancée | Étendue |

Les quotas et fonctionnalités sont centralisés au niveau du système de souscription.

Exemples de limites pouvant être contrôlées :

```text
Nombre d'offres analysées
Nombre de matchings
Nombre de lettres générées
Nombre de candidatures
Fonctionnalités IA disponibles
```

> Les valeurs exactes des quotas doivent être définies dans la configuration métier de l'application.

---

# 🧠 Human-in-the-Loop

Le projet ne vise pas à remplacer complètement le candidat.

Le principe est :

```text
             AI
              │
     ┌────────┴────────┐
     │                 │
 Analyse           Recommendation
     │                 │
     └────────┬────────┘
              ▼
       👤 HUMAN REVIEW
              │
              ▼
        Final Decision
```

Les étapes sensibles doivent rester contrôlées par l'utilisateur.

### Validation obligatoire

- Informations extraites du CV
- Profil final
- Documents générés
- Candidature avant soumission

---

# 🏗️ Architecture

L'architecture cible est organisée autour de plusieurs composants indépendants.

```text
                        ┌──────────────────────┐
                        │      Frontend        │
                        │     Streamlit        │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │       Backend        │
                        │       FastAPI        │
                        └──────────┬───────────┘
                                   │
             ┌─────────────────────┼─────────────────────┐
             │                     │                     │
             ▼                     ▼                     ▼
     ┌──────────────┐      ┌──────────────┐     ┌──────────────┐
     │  PostgreSQL  │      │  AI Services │     │ Job Sources  │
     │   Database   │      │              │     │              │
     └──────────────┘      └──────┬───────┘     └──────────────┘
                                  │
                         ┌────────┴────────┐
                         │                 │
                         ▼                 ▼
                    Matching            LLM
```

---

# 🛠️ Tech Stack

## Backend

| Technologie | Utilisation |
|---|---|
| **FastAPI** | API REST |
| **SQLAlchemy** | ORM |
| **Pydantic v2** | Validation des données |
| **JWT** | Authentification |
| **Python** | Langage principal |

Port cible :

```text
http://localhost:8000
```

---

## Frontend

| Technologie | Utilisation |
|---|---|
| **Streamlit** | Interface utilisateur |
| **CSS** | Design et personnalisation |
| **Python** | Logique UI |

Port cible :

```text
http://localhost:8501
```

---

## Database

```text
PostgreSQL 16
```

Image Docker :

```text
postgres:16-alpine
```

Port :

```text
5432
```

---

## Infrastructure

```text
Docker
Docker Compose
```

---

# 📁 Project Structure

```text
INTERVIEW-GUARANTEED/
│
├── backend/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   │
│   │   ├── main.py
│   │   │   └── FastAPI entry point
│   │   │
│   │   ├── config.py
│   │   │   └── Centralized configuration
│   │   │
│   │   ├── database.py
│   │   │   └── PostgreSQL / SQLAlchemy configuration
│   │   │
│   │   ├── models.py
│   │   │   └── SQLAlchemy ORM models
│   │   │
│   │   ├── schemas.py
│   │   │   └── Pydantic request/response schemas
│   │   │
│   │   ├── security.py
│   │   │   └── Password hashing / JWT / authentication
│   │   │
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   ├── auth.py
│   │   │   ├── cv.py
│   │   │   ├── jobs.py
│   │   │   └── applications.py
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── matching.py
│   │       ├── letters.py
│   │       └── stop_rule.py
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── assets/
│   │   ├── styles.css
│   │   └── ambient_motion.html
│   │
│   ├── components/
│   │   ├── __init__.py
│   │   └── ui.py
│   │
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
└── README.md
```

---

# 🔄 Application Workflow

## Complete workflow

```text
                    ┌──────────────┐
                    │   Register   │
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ Upload CV    │
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ Parse CV     │
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ Human Review │
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ Profile      │
                    │ Validated    │
                    └──────┬───────┘
                           ▼
                 ┌────────────────────┐
                 │ Collect Job Offers │
                 └──────────┬─────────┘
                            ▼
                 ┌────────────────────┐
                 │ Normalize Offers   │
                 └──────────┬─────────┘
                            ▼
                 ┌────────────────────┐
                 │ Matching Engine    │
                 └──────────┬─────────┘
                            ▼
                 ┌────────────────────┐
                 │ Ranked Job Offers  │
                 └──────────┬─────────┘
                            ▼
                 ┌────────────────────┐
                 │ Generate Letter    │
                 └──────────┬─────────┘
                            ▼
                 ┌────────────────────┐
                 │ Human Validation   │
                 └──────────┬─────────┘
                            ▼
                 ┌────────────────────┐
                 │ Application        │
                 └──────────┬─────────┘
                            ▼
                 ┌────────────────────┐
                 │ Track Status       │
                 └──────────┬─────────┘
                            ▼
                    ┌──────────────┐
                    │  Interview?  │
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              │                         │
             YES                       NO
              │                         │
              ▼                         ▼
       ┌──────────────┐        ┌────────────────┐
       │ Agent STOP   │        │ Continue Search│
       │   ARRETE     │        └────────────────┘
       └──────────────┘
```

---

# 🗃️ Data Model

Le modèle de données principal repose sur les entités suivantes :

```text
User
 │
 ├── Consent
 │
 ├── Subscription
 │
 ├── CvProfile
 │      ├── Skills
 │      ├── Experiences
 │      ├── Education
 │      └── Languages
 │
 ├── JobOffer
 │
 └── Application
         │
         └── Cover Letter
```

## Core Entities

### User

Représente le candidat utilisant la plateforme.

### Consent

Conserve les informations relatives au consentement et aux traitements de données.

### Subscription

Représente la formule utilisée par le candidat.

### CvProfile

Contient le profil professionnel validé.

### JobOffer

Représente une offre d'emploi normalisée.

### Application

Représente une candidature et son état.

---

# 🔐 Security & Privacy

La sécurité est un élément central du projet.

## Authentication

L'authentification repose sur :

```text
JWT
+
Password Hashing
+
Protected API Routes
```

Les mots de passe ne doivent jamais être stockés en clair.

---

## Environment Secrets

Les informations sensibles ne doivent pas être stockées directement dans le code source.

Exemple :

```env
DATABASE_URL=...
JWT_SECRET=...
LLM_API_KEY=...
```

Le fichier `.env` doit rester hors du dépôt Git.

---

# ⚖️ Privacy & Compliance

Le projet est conçu en tenant compte des principes associés à :

- **Law 09-08**
- **GDPR**

Les principes importants sont notamment :

```text
Explicit Consent
      │
      ▼
Data Minimization
      │
      ▼
Secure Processing
      │
      ▼
Traceability
      │
      ▼
Right to Erasure
```

Le système doit permettre de gérer les consentements et les demandes de suppression de données conformément aux règles retenues pour le projet.

---

# 🧩 Backend

Le backend FastAPI est organisé selon une séparation entre :

```text
Routers
   │
   ▼
Business Logic
   │
   ▼
Services
   │
   ▼
Database
```

## Routers

### `health.py`

Gestion des vérifications de santé de l'application et de la base de données.

### `auth.py`

Responsable notamment de :

- inscription ;
- connexion ;
- authentification ;
- profil ;
- consentement ;
- workflows liés à la suppression.

### `cv.py`

Responsable de :

- upload ;
- parsing ;
- structuration ;
- validation humaine.

### `jobs.py`

Responsable de :

- offres ;
- normalisation ;
- matching ;
- score ;
- explication.

### `applications.py`

Responsable de :

- candidatures ;
- lettres ;
- quotas ;
- statuts ;
- règle d'arrêt.

---

# 🧠 AI Services

## `matching.py`

Contient la logique du moteur de matching.

Responsabilités :

```text
Profile
   +
Job Offer
   │
   ▼
Feature Extraction
   │
   ▼
Similarity
   │
   ▼
Weighted Score
   │
   ▼
Explanation
```

---

## `letters.py`

Gère la génération des lettres de motivation.

Principe fondamental :

```text
Validated Profile
       +
Job Offer
       │
       ▼
    LLM
       │
       ▼
Cover Letter
```

Le service doit empêcher l'utilisation d'informations non validées.

---

## `stop_rule.py`

Centralise les règles relatives à :

- quotas ;
- état de l'agent ;
- `ACTIF` ;
- `ARRETE` ;
- détection de l'entretien ;
- blocage de nouvelles candidatures.

---

# 🗄️ Database

Le projet utilise :

```text
PostgreSQL 16
```

avec :

```text
SQLAlchemy ORM
```

La couche de persistance doit permettre de conserver notamment :

```text
Users
Consents
Subscriptions
CV Profiles
Job Offers
Matchings
Applications
Cover Letters
Activity Logs
```

---

# 🐳 Docker

L'environnement de développement est prévu pour fonctionner avec Docker Compose.

Architecture :

```text
Docker Compose
│
├── backend
│     └── FastAPI
│
├── frontend
│     └── Streamlit
│
└── database
      └── PostgreSQL 16
```

## Build

```bash
docker compose build
```

## Start

```bash
docker compose up -d
```

## Stop

```bash
docker compose down
```

## Logs

```bash
docker compose logs -f
```

Pour un service particulier :

```bash
docker compose logs -f backend
```

---

# ⚙️ Configuration

La configuration doit être centralisée afin d'éviter de disperser les paramètres métier et techniques dans le code.

Exemples de paramètres :

```text
DATABASE_URL
JWT_SECRET
JWT_ALGORITHM
JWT_EXPIRATION
LLM_API_KEY
MATCHING_SEMANTIC_WEIGHT
MATCHING_SKILLS_WEIGHT
MATCHING_PREFERENCES_WEIGHT
APPLICATION_QUOTA
LETTER_QUOTA
AGENT_STATUS
```

### Matching weights

```text
SEMANTIC_WEIGHT      = 0.45
SKILLS_WEIGHT        = 0.35
PREFERENCES_WEIGHT   = 0.20
```

La somme doit rester égale à :

```text
1.00
```

---

# 🚀 Development

## 1. Clone the repository

```bash
git clone <repository-url>
cd INTERVIEW-GUARANTEED
```

## 2. Configure environment variables

Créer un fichier :

```text
.env
```

et renseigner les variables nécessaires au projet.

## 3. Start the application

```bash
docker compose up --build
```

## 4. Access the services

Frontend :

```text
http://localhost:8501
```

Backend :

```text
http://localhost:8000
```

API documentation :

```text
http://localhost:8000/docs
```

> Les URLs et ports correspondent à l'architecture cible définie pour le projet et peuvent être adaptés à la configuration réelle de l'implémentation.

---

# 🧪 Testing

Le projet doit être testé à plusieurs niveaux.

## Unit Tests

Tester individuellement :

```text
Matching Engine
CV Parser
Quota Management
Stop Rule
Validation
Authentication
```

---

## Integration Tests

Tester les interactions :

```text
Frontend
   ↓
Backend
   ↓
Database
```

et :

```text
Backend
   ↓
AI Services
```

---

## Business Rule Tests

Exemples de scénarios critiques :

### Scenario 1 — CV validation

```text
Upload CV
   ↓
Extract profile
   ↓
Human validation
   ↓
Profile accepted
```

### Scenario 2 — Matching

```text
Profile + Job
      ↓
45 / 35 / 20
      ↓
Score
      ↓
Explanation
```

### Scenario 3 — Interview

```text
Application
     ↓
Interview Obtained
     ↓
Agent = ARRETE
     ↓
New Applications Blocked
```

### Scenario 4 — Hallucination prevention

```text
Information absent from validated profile
              ↓
       Must NOT appear
              ↓
       Generated Letter
```

---

# 🔌 API Overview

L'API est organisée par domaines fonctionnels.

| Module | Responsabilité |
|---|---|
| `/health` | Health checks |
| `/auth` | Authentication and user management |
| `/cv` | CV upload, parsing and validation |
| `/jobs` | Job offers and matching |
| `/applications` | Applications, letters and statuses |

La documentation interactive de FastAPI sera disponible via :

```text
/docs
```

lorsque le backend est lancé.

---

# 📊 Business State Machine

L'état global de l'agent est volontairement simple :

```text
                 ┌──────────┐
                 │  ACTIF   │
                 └────┬─────┘
                      │
                      │ Interview obtained
                      ▼
                 ┌──────────┐
                 │  ARRETE  │
                 └──────────┘
```

Une fois dans :

```text
ARRETE
```

l'agent ne doit plus déclencher automatiquement de nouvelles candidatures.

---

# 📈 Development Roadmap

## Phase 1 — Conception

- [x] Cahier des charges
- [x] Définition des règles métier
- [x] Architecture cible
- [x] Modélisation UML
- [x] Modèle de données
- [x] Définition du matching

---

## Phase 2 — Backend

- [ ] Initialisation FastAPI
- [ ] Configuration PostgreSQL
- [ ] SQLAlchemy models
- [ ] Authentication
- [ ] JWT
- [ ] User management
- [ ] Consent management
- [ ] CV upload
- [ ] CV parsing
- [ ] Profile validation

---

## Phase 3 — Job Engine

- [ ] Job source integration
- [ ] Job normalization
- [ ] Deduplication
- [ ] Matching engine
- [ ] Explainable score
- [ ] Ranking

---

## Phase 4 — AI Generation

- [ ] LLM integration
- [ ] Prompt design
- [ ] CV-grounded generation
- [ ] Hallucination controls
- [ ] Letter validation
- [ ] Version management

---

## Phase 5 — Applications

- [ ] Application management
- [ ] Status tracking
- [ ] Quota management
- [ ] Stop rule
- [ ] Interview detection / registration
- [ ] Activity logging

---

## Phase 6 — Frontend

- [ ] Authentication interface
- [ ] Candidate profile
- [ ] CV upload
- [ ] Profile validation
- [ ] Job dashboard
- [ ] Matching visualization
- [ ] Cover letter interface
- [ ] Application tracking
- [ ] Subscription management

---

## Phase 7 — Testing & Documentation

- [ ] Unit tests
- [ ] Integration tests
- [ ] Business rule tests
- [ ] Security checks
- [ ] Documentation
- [ ] Demonstration
- [ ] Final report

---

# 📌 Project Status

> 🚧 **Status: In Development**

The repository currently defines the target architecture and business rules for the **Entretien Garanti** platform.

The implementation is expected to follow the architecture and specifications documented in this README and in the project's design documentation.

---

# 🔮 Future Improvements

Once the MVP is stable, the following extensions can be considered:

### 📄 CV Optimization

Automatically suggest adaptations to the CV based on a selected job offer while preserving factual accuracy.

### 🎤 Interview Preparation

Generate interview questions based on:

```text
Job Description
+
Validated Candidate Profile
```

### 📧 Notifications

Possible future integrations:

- email notifications ;
- application status alerts ;
- interview reminders.

### 🌍 Multilingual Support

Potential support for:

```text
🇫🇷 Français
🇬🇧 English
🇲🇦 العربية
```

### 📊 Advanced Analytics

Possible dashboard metrics:

```text
Applications sent
Response rate
Interview rate
Average matching score
Top skills requested
Most successful job categories
```

---

# 🧭 Design Philosophy

The project follows five major principles:

```text
┌─────────────────────────────────────────┐
│             ENTRETENIR GARANTI          │
├─────────────────────────────────────────┤
│                                         │
│  👤 Human Control                       │
│  🧠 Explainable AI                      │
│  🛡️  Grounded Generation                │
│  🔐 Privacy by Design                   │
│  🛑 Automatic Stop Rule                 │
│                                         │
└─────────────────────────────────────────┘
```

The objective is not simply to build an AI that generates applications.

The objective is to build a **controlled, explainable and auditable AI agent** capable of assisting the candidate throughout the job-search process while keeping the candidate responsible for the final decisions.

---

# 📚 Documentation

The project documentation should progressively include:

```text
docs/
├── requirements/
│   └── cahier-des-charges.md
│
├── uml/
│   ├── use-case.md
│   ├── class-diagram.md
│   ├── sequence-diagrams.md
│   ├── activity-diagram.md
│   └── state-diagram.md
│
├── architecture/
│   └── architecture.md
│
├── ai/
│   ├── matching.md
│   └── generation.md
│
└── database/
    └── data-model.md
```

---

# 🤝 Contribution

Les contributions peuvent suivre le workflow Git classique :

```bash
git checkout -b feature/<feature-name>
```

Développer la fonctionnalité, puis :

```bash
git add .
git commit -m "feat: add <feature>"
git push origin feature/<feature-name>
```

Les changements importants doivent être documentés et accompagnés de tests lorsque cela est pertinent.

---

# 📄 License

This project is developed for academic and educational purposes.

The final licensing terms should be defined by the project authors before public distribution.

---

## 👨‍💻 Authors

**Entretien Garanti — AI Career & Job Application Management Platform**

Developed as an academic Data Science / Artificial Intelligence project.

> **Human in the loop. Explainable by design. Grounded in facts. Stopped at the right moment.**