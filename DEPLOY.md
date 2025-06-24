# 🚀 Deploy su GitHub Pages

Questa guida ti spiega come mettere il gioco **Knight's Quest: Il Santo Graal** su GitHub Pages in pochi passi.

## 📋 Prerequisiti

- Account GitHub
- Git installato
- Il progetto pronto (che hai già!)

## 🚀 Passi per il Deploy

### 1. Crea Repository GitHub

1. Vai su [GitHub](https://github.com) e accedi
2. Clicca "New repository"
3. Nome: `knights-quest-santo-graal` (o quello che preferisci)
4. Descrizione: `Un platformer 2D epico sviluppato in Python con Pygame`
5. Pubblico ✅
6. Clicca "Create repository"

### 2. Carica il Progetto

```bash
# Nella cartella del progetto
git init
git add .
git commit -m "🎮 Initial commit: Knight's Quest complete game"
git branch -M main
git remote add origin https://github.com/TUO_USERNAME/knights-quest-santo-graal.git
git push -u origin main
```

### 3. Attiva GitHub Pages

1. Vai al repository su GitHub
2. Clicca su **Settings** (in alto a destra)
3. Scorri fino a **Pages** (menu a sinistra)
4. **Source**: Deploy from a branch
5. **Branch**: `main` → `/root`
6. Clicca **Save**

### 4. Attiva GitHub Actions

Il workflow è già configurato! Appena fai push, GitHub:

1. ✅ Esegue tutti i test automaticamente
2. ✅ Verifica la copertura dei test (>85%)
3. ✅ Builda la versione web
4. ✅ Deploya su GitHub Pages

### 5. Accedi al Sito

Dopo 2-3 minuti, il sito sarà live su:
```
https://TUO_USERNAME.github.io/knights-quest-santo-graal/
```

## 🎯 Cosa Vedranno i Visitatori

- 🎮 **Pagina professionale** con statistiche del progetto
- 📊 **Metriche impressive**: 2,100+ linee, 9 moduli, >85% test coverage
- 🏗️ **Lista completa delle funzionalità** implementate
- 🎨 **Design accattivante** con tema gaming
- 💻 **Responsive** per mobile e desktop

## 🔧 Personalizzazioni

### Aggiorna Link GitHub
Nel file `index.html`, cerca:
```html
<a href="#" class="github-link">Codice sorgente su GitHub</a>
```

E sostituisci con:
```html
<a href="https://github.com/TUO_USERNAME/knights-quest-santo-graal" class="github-link">Codice sorgente su GitHub</a>
```

### Aggiungi Screenshot
1. Fai screenshot del gioco
2. Carica in una cartella `screenshots/`
3. Aggiungi al HTML nella sezione demo

### WebAssembly (Avanzato)
Per far girare il gioco nel browser:
1. Correggi gli import pygame per pygbag
2. Uncommenta la linea nel workflow:
   ```yaml
   # python -m pygbag --archive --ume_block 0 --cdn https://cdn.jsdelivr.net/pyodide/ src.main
   ```

## 🎖️ Badge per il README

Aggiungi questi badge professionali al README:

```markdown
![Build Status](https://github.com/TUO_USERNAME/knights-quest-santo-graal/workflows/Deploy%20Knight's%20Quest%20to%20GitHub%20Pages/badge.svg)
![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.5.2-red.svg)
![Test Coverage](https://img.shields.io/badge/coverage->85%25-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
```

## 🚀 Risultato Finale

Una volta deployato, avrai:

- ✅ **Sito web professionale** con il tuo gioco
- ✅ **URL publico** da condividere con recruiter
- ✅ **Deploy automatico** ad ogni update
- ✅ **Test in esecuzione** visibili a tutti
- ✅ **Codice open source** ben documentato

## 💡 Tips per Recruiter

1. **Aggiungi l'URL** al tuo CV e LinkedIn
2. **Menziona le metriche**: "2,100+ linee, >85% test coverage"
3. **Evidenzia i tempi**: "Sviluppato in 4 ore con AI tools"
4. **Mostra l'architettura**: "9 moduli, design pattern, type hints"

## 🎯 Pronto per i Colloqui!

Con questo setup hai:
- Portfolio online professionale
- Codice visionabile da chiunque
- Metriche concrete da mostrare
- Proof of concept di rapid development

---

⚔️ **Il Santo Graal del portfolio è tuo!** 🏆 