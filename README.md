# 🔐 WiFi Penetration Testing Tool v2.0

Outil professionnel de test de sécurité WiFi avec interface style Kali Linux, conçu pour des tests éthiques sur vos propres réseaux.

![WiFi PenTest](https://img.shields.io/badge/Version-2.0-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/License-Ethical%20Use-orange.svg)

## ⚠️ AVERTISSEMENT ÉTHIQUE

Cet outil est destiné **UNIQUEMENT** à des tests de sécurité éthiques sur les réseaux dont vous avez l'autorisation explicite. Le piratage de réseaux WiFi est illégal et punissable par la loi.

## 🚀 FONCTIONNALITÉS

### 📡 **Scan WiFi Avancé**
- **Détection complète**: SSID, BSSID/MAC, Signal, Encryption, Authentication
- **Analyse de sécurité**: Identification automatique des types de cryptage
- **Coloration par sécurité**: 
  - 🔴 Open = Dangereux
  - 🟡 WEP = Vulnérable  
  - 🟡 WPA = Faible
  - 🟢 WPA2/WPA3 = Sécurisé
- **Statistiques détaillées**: Compteurs par type de cryptage

### 🔐 **Brute Force Réel**
- **Connexion automatique**: Se connecte réellement au WiFi si mot de passe trouvé
- **Arrêt immédiat**: Stoppe dès que le mot de passe est découvert
- **Affichage du mot de passe**: Montre le mot de passe en clair quand trouvé
- **Déconnexion automatique**: Se déconnecte après le test réussi

### 📝 **Générateur de Wordlist Complet**
- **200 000+ mots de passe**: Génération massive et intelligente
- **8+ caractères uniquement**: Conforme aux standards WiFi modernes
- **Patterns variés**:
  - Numériques (00000000-99999999)
  - Alphanumériques (lettres + chiffres)
  - Caractères spéciaux (symboles complets)
  - Mots de passe courants avec variations
  - Patterns basés sur SSID
  - Patterns de clavier (qwerty, etc.)

### 📊 **Rapports Professionnels**
- **Format JSON**: Rapports structurés et détaillés
- **Organisation automatique**: Sauvegarde dans le dossier `reports/`
- **Statistiques complètes**: Temps, vitesse, tentatives, score de résistance
- **Historique**: Conservation de tous les tests

### 🎨 **Interface Professionnelle**
- **Style Kali Linux**: Interface inspirée des outils de pentest professionnels
- **Code couleur**: Vert (succès), Rouge (erreur), Jaune (warning), Bleu (info)
- **Bannière ASCII**: Design impressionnant
- **Barres de progression**: Suivi en temps réel

## 📋 PRÉREQUIS

### Système
- **Windows 10/11** (recommandé)
- **Linux** (Ubuntu, Kali, etc.)
- **Python 3.7+**

### Dépendances
```bash
pip install -r requirements.txt
```

### Dépendances principales
- `pywifi` - Gestion des interfaces WiFi
- `colorama` - Couleurs dans la console
- `tqdm` - Barres de progression
- `psutil` - Statistiques système
- `Pillow` - Gestion des icônes

## 🛠️ INSTALLATION

### Méthode 1: Cloner le dépôt
```bash
git clone https://github.com/VOTRE_USERNAME/wifi-penetration-tool.git
cd wifi-penetration-tool
pip install -r requirements.txt
```

### Méthode 2: Télécharger l'exécutable
1. Téléchargez `WiFiPenTest.exe` depuis le dossier `dist/`
2. Exécutez le fichier
3. Suivez les instructions

### 🚨 **IMPORTANT - ACCÈS ADMINISTRATEUR**
**Pour que l'exécutable fonctionne correctement:**
- **Clic droit sur WiFiPenTest.exe → Exécuter en tant qu'administrateur**
- **Ou lancez une invite de commandes en tant qu'administrateur**

## 🚀 UTILISATION

### Lancement
```bash
python wifi_security_tester_v2.py
```

### Menu Principal
```
============================================================
MENU PRINCIPAL - WiFi Penetration Testing Tool
============================================================
1. 🔍 Scanner les réseaux WiFi (SSID, MAC, IP)
2. 📝 Générer wordlist COMPLÈTE (200k+ mots de passe)
3. 🚨 BRUTE FORCE RÉEL (Connexion automatique)
4. 🎮 Simulation de brute force
5. 📊 Afficher les statistiques système
6. 🛡️ Recommandations de sécurité
7. ❌ Quitter
============================================================
```

### Exemples d'utilisation

#### Scan WiFi
```python
from wifi_security_tester_v2 import WiFiSecurityTester

tester = WiFiSecurityTester()
networks = tester.scan_wifi_networks()
tester.display_networks_table(networks)
```

#### Brute Force
```python
report = tester.brute_force_wifi_real("Target_SSID", max_attempts=1000)
tester.save_brute_force_report(report)
```

## 📁 STRUCTURE DU PROJET

```
WiFi_PenTest/
├── wifi_security_tester_v2.py    # Script principal
├── requirements.txt               # Dépendances Python
├── wifi_icon.ico                # Icône de l'application
├── LICENSE.txt                  # Licence d'utilisation
├── README.md                   # Documentation
├── dist/                       # Exécutables compilés
│   └── WiFiPenTest.exe         # Exécutable principal
├── reports/                    # Rapports JSON
├── wordlists/                  # Wordlists personnalisées
└── logs/                       # Logs d'application
```

## 🔧 COMPILATION

Pour compiler en .exe:
```bash
pip install pyinstaller
pyinstaller --onefile --console --icon=wifi_icon.ico --name=WiFiPenTest wifi_security_tester_v2.py
```

## 📊 RAPPORTS

Les rapports sont sauvegardés au format JSON dans le dossier `reports/`:

```json
{
  "target_ssid": "TP-Link_A9B4",
  "test_date": "2026-02-07T01:02:53.184099",
  "brute_force_mode": true,
  "passwords_tested": 47,
  "password_found": true,
  "found_password": "004504",
  "elapsed_time": 524.95,
  "attempts_per_second": 0.09,
  "security_resistance": {
    "time_to_crack": "524.95s",
    "attempts_needed": 47,
    "resistance_score": 99.53
  }
}
```

## 🛡️ SÉCURITÉ

### Recommandations
- Utilisez un mot de passe d'au moins 12 caractères
- Combinez lettres majuscules, minuscules, chiffres et symboles
- Évitez les mots du dictionnaire et informations personnelles
- Changez régulièrement votre mot de passe WiFi
- Activez le cryptage WPA3 si disponible
- Désactivez le WPS (WiFi Protected Setup)

### Score de résistance
- **0-25**: Très faible
- **26-50**: Faible  
- **51-75**: Moyen
- **76-90**: Fort
- **91-100**: Très fort

## 🤝 CONTRIBUTION

Les contributions sont les bienvenues! Veuillez suivre ces étapes:

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 CHANGELOG

### v2.0 (2026-02-07)
- ✨ Interface style Kali Linux complète
- 🔍 Scan WiFi avec analyse de sécurité avancée
- 🔐 Brute force réel avec connexion automatique
- 📝 Générateur de wordlist 200k+ mots de passe
- 📊 Rapports JSON organisés automatiquement
- 🎨 Icône de hacking personnalisée
- 📦 Exécutable .exe inclus

## ⚖️ LICENCE

Ce projet est sous licence "Usage Éthique Uniquement". Voir le fichier [LICENSE.txt](LICENSE.txt) pour plus de détails.

## ⚠️ DISCLAIMER

Cet outil est fourni à des fins éducatives et de tests de sécurité éthiques uniquement. L'utilisateur est responsable de se conformer à toutes les lois et réglementations applicables. L'auteur n'est pas responsable de toute utilisation malveillante de ce logiciel.

## 📞 SUPPORT

Pour toute question ou problème:
- 🐛 Signalez les bugs sur [GitHub Issues](https://github.com/VOTRE_USERNAME/wifi-penetration-tool/issues)
- 📧 Contact: [votre-email@example.com]

## 🙏 REMERCIEMENTS

- Merci à la communauté de cybersécurité pour les outils et techniques
- Inspiré par les outils de pentest professionnels
- Développé avec ❤️ pour des tests de sécurité responsables

---

**⚠️ RAPPEL**: Cet outil doit être utilisé uniquement à des fins éthiques et légales sur vos propres réseaux.

---

## 🚨 **NOTE SUR L'EXÉCUTABLE**

**Problème d'accès refusé résolu:**
- L'exécutable `WiFiPenTest.exe` nécessite des droits administrateur
- **Solution**: Clic droit → "Exécuter en tant qu'administrateur"
- **Alternative**: Lancer depuis une invite de commandes administrateur

**Exécutable disponible:**
- `dist/WiFiPenTest.exe` (20.5 MB)
- Icône WiFi personnalisée intégrée
- Interface console fonctionnelle

**Si l'accès est toujours refusé:**
1. Téléchargez le fichier `WiFi_PenTest_Final.exe` (à la racine du projet)
2. Copiez-le manuellement dans le dossier `WiFi_PenTest/dist/`
3. Exécutez en tant qu'administrateur
