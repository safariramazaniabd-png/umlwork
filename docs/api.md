# API Reference — HumanitAID

## Base URL

```
http://localhost:8000/api/v1
```

## Endpoints

### Donateurs

| Méthode | Chemin               | Description         |
|---------|----------------------|---------------------|
| POST    | `/donateurs/`        | Créer un donateur   |
| GET     | `/donateurs/`        | Lister les donateurs|
| GET     | `/donateurs/{id}`    | Donateur par ID     |
| PATCH   | `/donateurs/{id}`    | Modifier un donateur|
| DELETE  | `/donateurs/{id}`    | Supprimer un donateur|

### Campagnes

| Méthode | Chemin               | Description          |
|---------|----------------------|----------------------|
| POST    | `/campagnes/`        | Créer une campagne   |
| GET     | `/campagnes/`        | Lister les campagnes |
| GET     | `/campagnes/{id}`    | Campagne par ID      |
| PATCH   | `/campagnes/{id}`    | Modifier une campagne|
| DELETE  | `/campagnes/{id}`    | Supprimer une campagne|

Paramètres GET : `?statut=active&skip=0&limit=100`

### Dons

| Méthode | Chemin          | Description       |
|---------|-----------------|-------------------|
| POST    | `/dons/`        | Créer un don      |
| GET     | `/dons/`        | Lister les dons   |
| GET     | `/dons/{id}`    | Don par ID        |
| DELETE  | `/dons/{id}`    | Supprimer un don  |

Paramètres GET : `?donateur_id=1&campagne_id=1`

### Paiements

| Méthode | Chemin             | Description          |
|---------|--------------------|----------------------|
| POST    | `/paiements/`      | Créer un paiement    |
| GET     | `/paiements/`      | Lister les paiements |
| GET     | `/paiements/{id}`  | Paiement par ID      |

### Reçus

| Méthode | Chemin          | Description       |
|---------|-----------------|-------------------|
| POST    | `/recus/`       | Générer un reçu   |
| GET     | `/recus/`       | Lister les reçus  |
| GET     | `/recus/{id}`   | Reçu par ID       |

## Modèles

### Donateur

```json
{
  "id": 1,
  "nom": "Dupont",
  "prenom": "Jean",
  "email": "jean@example.com",
  "telephone": "+33600000000",
  "pays": "France",
  "type_compte": "enregistre",
  "date_inscription": "2026-06-26T10:00:00Z",
  "est_actif": true
}
```

### Campagne

```json
{
  "id": 1,
  "titre": "Aide aux sinistrés",
  "description": "Campagne d'urgence",
  "objectif": 50000.0,
  "montant_collecte": 12300.0,
  "date_debut": "2026-06-01T00:00:00Z",
  "date_fin": "2026-07-01T00:00:00Z",
  "statut": "active",
  "progression": 24.6
}
```

### Don

```json
{
  "id": 1,
  "montant": 100.0,
  "devise": "EUR",
  "date": "2026-06-26T10:00:00Z",
  "frequence": "ponctuel",
  "statut": "confirme",
  "donateur_id": 1,
  "campagne_id": 1
}
```
