# Knight's Quest: Il Santo Graal 🗡️⚔️

Un platformer 2D completo sviluppato in Python con Pygame, dove un cavaliere affronta demoni e raccoglie risorse per ottenere il Santo Graal.


## 🔍 Sviluppo Assistito da AI

Il progetto è stato interamente sviluppato con l’ausilio di Cursor (AI-powered IDE), sfruttando il supporto di modelli LLM per:

- Refactoring continuo del codice
- Generazione di test e debugging
- Ottimizzazione dell’architettura modulare
- Miglioramento della documentazione inline e README

Questo approccio ha permesso una produttività più alta e una maggiore attenzione alla qualità del codice.


## 🎯 Obiettivo del Gioco

Gioca nei panni di un coraggioso cavaliere che deve:
- ⚔️ Sconfiggere demoni malvagi
- 💰 Raccogliere risorse preziose (Oro, Argento, Mirra)
- 🐍 Battere il boss finale: il Serpente Cornuto
- 🏆 Ottenere il Santo Graal

## 🎮 Comandi di Gioco

- **Frecce ← →**: Movimento orizzontale
- **SPAZIO**: Salto
- **X**: Attacco con spada
- **P**: Pausa/Riprendi
- **ESC**: Menu principale
- **ENTER**: Inizia gioco (dal menu)
- **R**: Riavvia (se Game Over)

## 🏗️ Struttura del Progetto

```
gioco cavaliere/
├── src/
│   ├── __init__.py          # Package Python
│   ├── config.py            # Configurazioni globali del gioco
│   ├── player.py            # Classe cavaliere protagonista
│   ├── enemy.py             # Sistema nemici e IA
│   ├── collectible.py       # Sistema oggetti raccoglibili
│   ├── platform.py          # Piattaforme e elementi di livello
│   ├── level.py             # Gestione livelli e progressione
│   ├── sprite_manager.py    # Gestione asset grafici
│   ├── game.py              # Game engine principale
│   └── main.py              # Entry point
├── sprites/
│   ├── cavaliereariposo.png # Sprite cavaliere statico
│   ├── cavaliereattacco.png # Sprite cavaliere in attacco
│   ├── demone.png           # Sprite nemico demone
│   ├── boss.png             # Sprite boss finale
│   ├── fondale1.png         # Background livello 1
│   ├── fondale2.png         # Background livello 2
│   ├── fondale3.png         # Background livello 3
│   └── fondale 4.png        # Background livello 4
├── tests/
│   ├── __init__.py
│   ├── test_player.py       # Test classe Player
│   ├── test_enemy.py        # Test sistema nemici
│   ├── test_collectible.py  # Test oggetti raccoglibili
│   ├── test_platform.py     # Test piattaforme
│   └── test_game.py         # Test game engine
├── pyproject.toml           # Configurazione progetto Python
├── requirements.txt         # Dipendenze Python
└── README.md               # Questo file
```

## 🚀 Installazione e Avvio

### Prerequisiti
- Python 3.11+
- pygame

### Installazione

1. **Clona il repository:**
```bash
git clone <repository-url>
cd "dioco cavaliere"
```

2. **Installa le dipendenze:**
```bash
pip install -r requirements.txt
```

3. **Avvia il gioco:**
```bash
python -m src.main
```

## 🧪 Test

Il progetto include una suite completa di test unitari con copertura superiore all'85%:

```bash
# Esegui tutti i test
python -m pytest tests/ -v

# Test con copertura dettagliata
python -m pytest tests/ --cov=src --cov-report=html

# Test specifici per modulo
python -m pytest tests/test_player.py -v
python -m pytest tests/test_enemy.py -v
python -m pytest tests/test_collectible.py -v
python -m pytest tests/test_platform.py -v
python -m pytest tests/test_game.py -v
```

## 🎨 Funzionalità Implementate

### ✅ Sistema Core
- [x] **Cavaliere Protagonista**: Movimento fluido, salto, attacco
- [x] **Sistema Nemici**: IA demoni con stati (Patrol, Chase, Attack)
- [x] **Sistema Combattimento**: Collisioni, danni, sistema HP
- [x] **Oggetti Raccoglibili**: Oro, Argento, Mirra con effetti speciali
- [x] **Piattaforme**: Sistema piattaforme multiple per level design
- [x] **Sistema Livelli**: Gestione progressione e caricamento livelli
- [x] **Asset Manager**: Caricamento e gestione sprite dinamica

### 🎮 Gameplay
- [x] Menu principale interattivo
- [x] Sistema di movimento completo con animazioni
- [x] Combat system con collisioni accurate
- [x] Inventory system per risorse
- [x] Sistema di livelli multipli
- [x] Boss fight implementato
- [x] Stati di gioco completi (Menu, Gioco, Pausa, Game Over, Vittoria)

### 🔧 Aspetti Tecnici
- [x] **Architettura modulare**: 9 moduli specializzati
- [x] **Tipizzazione statica**: Type hints completi
- [x] **Test Coverage**: >85% su tutti i moduli principali
- [x] **Asset Pipeline**: Gestione centralizzata sprite
- [x] **Config Management**: Configurazioni centralizzate
- [x] **Error Handling**: Gestione robusta degli errori

## 🎨 Asset Grafici

Il gioco include sprite personalizzati ad alta risoluzione:
- **Cavaliere**: Animazioni riposo e attacco
- **Nemici**: Sprite demone e boss
- **Backgrounds**: 4 fondali tematici diversi
- **Dimensioni**: Asset ad alta qualità (1-3MB per sprite)

## 🧰 Tecnologie Utilizzate

- **Python 3.11+**: Linguaggio principale
- **pygame**: Game engine e rendering
- **pytest**: Testing framework completo
- **Type Hints**: Tipizzazione statica completa
- **Modular Design**: Architettura scalabile

## 📊 Statistiche del Progetto

- **Linee di codice**: ~2,100 linee
- **Moduli**: 9 moduli specializzati
- **Test Coverage**: >85%
- **Asset grafici**: 8 sprite ad alta risoluzione
- **Tempo di sviluppo**: 4 ore (con pausa)

## 🤝 Architettura

Il progetto segue best practices di game development:

1. **Separation of Concerns**: Ogni modulo ha responsabilità specifiche
2. **Entity-Component Pattern**: Separazione logica entità/comportamenti
3. **Event-Driven Design**: Gestione input e stati via eventi
4. **Asset Management**: Caricamento lazy e gestione memoria
5. **Test-Driven Development**: Test coverage completo

## 📄 Licenza

MIT License - Vedi LICENSE file per dettagli.

---

⚔️ **Il Santo Graal ti aspetta, cavaliere!** 🏆 

*Progetto sviluppato con Python, Pygame e strumenti di AI-assisted development.* 