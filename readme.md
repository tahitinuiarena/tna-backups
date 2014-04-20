## Backup TNA

Ce projet est écrit en python et utilise le framework fabric. Il vous faudra installer Python et Pip pour pouvoir utiliser ce logiciel.

### Installation des dépendances

```bash
pip install -r requirements.txt
```
Si vous voulez isoler ces dépendances, vous devriez installer virtualenv.

### Utilisation

```bash
fab dbbackup:dbpassword -u login -p password
```

