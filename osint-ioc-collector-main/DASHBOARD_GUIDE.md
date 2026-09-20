# IOC Collector Dashboard - Guide d'Utilisation

## 🎨 Interface Web Moderne

Le dashboard IOC Collector est une interface web moderne qui vous permet de visualiser, gérer et analyser vos indicateurs de compromission en temps réel.

## 🚀 Démarrage Rapide

### Lancer le Dashboard

```bash
cd /Users/ademmedjahed/Project/ioc-collector
./run_dashboard.sh
```

Ou manuellement:
```bash
source venv/bin/activate
python3 -m web.app
```

Le dashboard sera accessible à: **http://localhost:5000**

## 📊 Fonctionnalités

### Page d'Accueil (Dashboard)

**URL**: `http://localhost:5000/`

#### Statistiques en Temps Réel
- **Total IOCs Actifs**: Nombre total d'IOCs dans la base
- **URLs Malveillantes**: Compteur des URLs collectées
- **Hashes de Malware**: Nombre de hashes de fichiers malveillants
- **Adresses IP**: Compteur d'IPs et plages réseau

#### Graphiques Interactifs
1. **IOCs par Type** (Donut Chart)
   - Distribution des IOCs par type (URL, Hash, IP, Domain)
   - Pourcentages et valeurs absolues

2. **IOCs par Source** (Bar Chart)
   - Comparaison des sources de données
   - URLhaus, MalwareBazaar, Spamhaus, Feodo

#### Actions Rapides
- **🔄 Collect Now**: Lance une collecte immédiate
- **📄 Export CSV**: Exporte toutes les données en CSV
- **📋 Export JSON**: Exporte toutes les données en JSON

#### Activité Récente
- Historique des 20 dernières collectes
- Statut de succès/échec
- Nombre d'IOCs collectés, nouveaux, mis à jour
- Messages d'erreur si applicable

### Page Liste des IOCs

**URL**: `http://localhost:5000/iocs`

#### Fonctionnalités
- **Tableau paginé**: 50 IOCs par page
- **Filtrage en temps réel**:
  - Par type (URL, Hash, IP, Domain)
  - Par source (URLhaus, MalwareBazaar, Spamhaus, Feodo)
- **Colonnes affichées**:
  - Valeur de l'IOC (avec formatage monospace)
  - Type (badge coloré)
  - Type de menace
  - Source
  - Score de confiance (/100)
  - Dernière observation

#### Navigation
- Boutons Précédent/Suivant
- Indicateur de page actuelle
- Désactivation automatique aux extrémités

## 🎨 Design et Interface

### Thème Sombre Moderne
- **Couleurs principales**:
  - Fond primaire: `#0f172a` (bleu très sombre)
  - Fond secondaire: `#1e293b` (bleu sombre)
  - Texte principal: `#f1f5f9` (blanc cassé)
  - Accent bleu: `#3b82f6`

### Responsive Design
- Adapté aux écrans desktop
- Sidebar collapsible sur mobile
- Grilles flexibles pour les cartes

### Animations
- Transitions fluides sur les hover
- Notifications slide-in
- Loading spinners pour les actions

## 🔌 API Endpoints

### GET /api/stats
Retourne les statistiques globales de la base de données.

**Réponse**:
```json
{
  "success": true,
  "stats": {
    "total_active_iocs": 17545,
    "total_inactive_iocs": 0,
    "avg_confidence_score": 65.0,
    "by_type": {
      "url": 12858,
      "hash": 2970,
      "ip": 1717
    },
    "by_source": {
      "urlhaus": 12858,
      "malwarebazaar": 2970,
      "spamhaus_drop": 1712,
      "feodo": 5
    }
  }
}
```

### GET /api/iocs
Retourne la liste paginée des IOCs avec filtres optionnels.

**Paramètres**:
- `page` (int): Numéro de page (défaut: 1)
- `per_page` (int): IOCs par page (défaut: 50, max: 1000)
- `type` (string): Filtrer par type (url, hash, ip, domain)
- `source` (string): Filtrer par source

**Exemple**: `/api/iocs?page=2&per_page=50&type=url&source=urlhaus`

**Réponse**:
```json
{
  "success": true,
  "iocs": [...],
  "pagination": {
    "page": 2,
    "per_page": 50,
    "total": 12858,
    "pages": 258
  }
}
```

### POST /api/collect
Déclenche une collecte manuelle de tous les feeds.

**Réponse**:
```json
{
  "success": true,
  "message": "Collection started in background"
}
```

### POST /api/export
Déclenche un export des données.

**Body**:
```json
{
  "format": "csv"
}
```

**Réponse**:
```json
{
  "success": true,
  "message": "Exported 2 files",
  "files": [
    "data/exports/iocs_full_20260918_123456.csv",
    "data/exports/iocs_delta_20260917_20260918_123456.csv"
  ]
}
```

### GET /api/recent-activity
Retourne les 20 dernières exécutions de collecte.

**Réponse**:
```json
{
  "success": true,
  "activities": [
    {
      "source": "urlhaus",
      "status": "success",
      "iocs_collected": 12858,
      "iocs_new": 234,
      "iocs_updated": 12624,
      "timestamp": "2026-09-18T10:30:00",
      "error_message": null
    }
  ]
}
```

### GET /api/chart-data
Retourne les données pour les graphiques.

**Réponse**:
```json
{
  "success": true,
  "data": {
    "by_type": {...},
    "by_source": {...},
    "timeline": [...]
  }
}
```

## ⚙️ Configuration

Le dashboard utilise les mêmes fichiers de configuration que l'application CLI:

- `config/settings.json`: Paramètres généraux
- `config/feeds.json`: Configuration des feeds

### Port et Host

Par défaut, le dashboard écoute sur:
- **Host**: `0.0.0.0` (accessible depuis le réseau local)
- **Port**: `5000`

Pour changer le port, modifiez `web/app.py`:
```python
app.run(host='0.0.0.0', port=8080, debug=True)
```

### Mode Debug

En production, désactivez le mode debug:
```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

## 🔄 Rafraîchissement Auto

Le dashboard actualise automatiquement:
- **Statistiques**: Toutes les 30 secondes
- **Activité récente**: Toutes les 30 secondes
- **Graphiques**: Lors de la collecte

## 📱 Utilisation

### Workflow Typique

1. **Démarrer le dashboard**:
   ```bash
   ./run_dashboard.sh
   ```

2. **Accéder à l'interface**: Ouvrir http://localhost:5000

3. **Lancer une collecte**:
   - Cliquer sur "Collect Now"
   - Attendre 10-15 secondes
   - Les stats se mettent à jour automatiquement

4. **Explorer les IOCs**:
   - Aller sur "IOCs List"
   - Filtrer par type ou source
   - Paginer dans les résultats

5. **Exporter les données**:
   - Cliquer sur "Export CSV" ou "Export JSON"
   - Les fichiers sont créés dans `data/exports/`

### Surveillance Continue

Pour une surveillance en continu:
1. Laisser le dashboard ouvert dans un navigateur
2. Le scheduler CLI peut tourner en parallèle:
   ```bash
   ./run.sh --schedule
   ```
3. Le dashboard affichera les nouvelles collectes automatiquement

## 🔐 Sécurité

### Production

Pour un déploiement en production:

1. **Désactiver le mode debug**:
   ```python
   app.run(debug=False)
   ```

2. **Utiliser un serveur WSGI** (Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 web.app:create_app()
   ```

3. **Ajouter une authentification** (optionnel):
   - Flask-Login pour les utilisateurs
   - Flask-HTTPAuth pour l'API

4. **Reverse proxy** (Nginx):
   ```nginx
   server {
       listen 80;
       server_name ioc-dashboard.example.com;

       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
       }
   }
   ```

### Secret Key

Changez la clé secrète dans `web/app.py`:
```python
app.config['SECRET_KEY'] = 'votre-clé-secrète-aléatoire-ici'
```

## 🐛 Dépannage

### Le dashboard ne démarre pas

```bash
# Vérifier que Flask est installé
pip list | grep -i flask

# Réinstaller si nécessaire
pip install flask==3.0.0

# Vérifier les logs
python3 -m web.app
```

### Erreur "Database not found"

```bash
# Initialiser la base de données
./run.sh --init
```

### Port déjà utilisé

```bash
# Trouver le processus utilisant le port 5000
lsof -i :5000

# Tuer le processus
kill -9 <PID>

# Ou changer le port dans web/app.py
```

### Données ne se chargent pas

1. Vérifier que la base de données contient des IOCs:
   ```bash
   ./run.sh --stats
   ```

2. Vérifier les permissions:
   ```bash
   ls -la data/ioc.db
   ```

3. Consulter les logs du serveur Flask dans la console

## 📊 Personnalisation

### Ajouter un nouveau graphique

1. Ajouter le canvas dans `templates/index.html`:
   ```html
   <canvas id="monGraphique"></canvas>
   ```

2. Créer la fonction dans `static/js/dashboard.js`:
   ```javascript
   function createMonGraphique(data) {
       const ctx = document.getElementById('monGraphique');
       // ... configuration Chart.js
   }
   ```

### Modifier les couleurs

Éditer les variables CSS dans `static/css/style.css`:
```css
:root {
    --accent-blue: #votre-couleur;
}
```

## 🚀 Déploiement Production

### Docker (Optionnel)

Créer un `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "web.app:create_app()"]
```

Build et run:
```bash
docker build -t ioc-dashboard .
docker run -p 5000:5000 -v $(pwd)/data:/app/data ioc-dashboard
```

### Systemd Service

Créer `/etc/systemd/system/ioc-dashboard.service`:
```ini
[Unit]
Description=IOC Collector Dashboard
After=network.target

[Service]
Type=simple
User=votre-user
WorkingDirectory=/path/to/ioc-collector
ExecStart=/path/to/ioc-collector/venv/bin/python3 -m web.app
Restart=always

[Install]
WantedBy=multi-user.target
```

Activer:
```bash
sudo systemctl enable ioc-dashboard
sudo systemctl start ioc-dashboard
```

## 📝 Notes

- Le dashboard est conçu pour des environnements single-user
- Pour multi-utilisateurs, ajouter Flask-Login
- Les collectes via l'interface sont asynchrones
- Les exports sont synchrones mais rapides
- Le rafraîchissement auto utilise polling (pas de WebSocket)

---

**Dashboard Version**: 1.0.0
**Compatible avec**: IOC Collector v1.0.0
**Dernière mise à jour**: 2026-09-18
