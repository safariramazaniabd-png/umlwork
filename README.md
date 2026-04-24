# HumanitAID — Système de Gestion des Dons

> Plateforme de gestion des dons humanitaires permettant aux donateurs de contribuer à des campagnes et aux administrateurs de les gérer.

## 📋 Présentation

HumanitAID est une application de gestion de dons destinée aux organisations humanitaires. Elle permet :

- **Aux donateurs** : consulter des campagnes, effectuer des dons (ponctuels ou récurrents), recevoir des reçus fiscaux
- **Aux administrateurs** : gérer les campagnes, consulter les rapports financiers

## 🏗 Architecture

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐
│  Donateur   │────▶│   Système   │────▶│ Passerelle Pago. │
│  (Interface)│     │  HumanitAID │     │   (Stripe/PayPal)│
└─────────────┘     └──────┬──────┘     └──────────────────┘
                           │
                    ┌──────▼──────┐
                    │     BD      │
                    └─────────────┘
```

## 📦 Modules

| Module | Description |
|--------|-------------|
| **Donateur** | Gestion des profils (anonyme / enregistré) |
| **Don** | Traitement des dons ponctuels et récurrents |
| **Campagne** | Création et suivi des campagnes de collecte |
| **Paiement** | Intégration passerelle de paiement |
| **Recu** | Génération et envoi des reçus fiscaux |

## Use Cases

### Donateur Anonyme
- Consulter les campagnes
- Faire un don ponctuel
- Créer un compte

### Donateur Enregistré
- Consulter les campagnes
- Faire un don ponctuel
- Faire un don récurrent
- Consulter l'historique des dons

### Administrateur
- Gérer les campagnes
- Consulter les rapports financiers

## 📊 Diagrammes

Le projet contient les diagrammes UML suivants :

| Fichier | Description |
|---------|-------------|
| `cas_utilisation.puml.txt` | Diagramme des cas d'utilisation |
| `classes.puml.txt` | Diagramme de classes |
| `activites.puml.txt` | Diagramme d'activités (flux d'un don) |
| `sequence.puml.txt` | Diagramme de séquence |

## 🚀 Flux de don

1. **Consultation** — Le donateur consulte les campagnes disponibles
2. **Sélection** — Il choisit une campagne et saisit le montant
3. **Paiement** — Il sélectionne la méthode de paiement
4. **Validation** — La passerelle valide la transaction
5. **Confirmation** — Reçu PDF envoyé par email + notification administrateur

## 🛠 Technologies

- **Backend** : API REST
- **Base de données** : PostgreSQL
- **Passerelle paiement** : Stripe / PayPal
- **Email** : Service SMTP

## 📄 Licence

Ce projet est un modèle UML — implémentez selon vos besoins.