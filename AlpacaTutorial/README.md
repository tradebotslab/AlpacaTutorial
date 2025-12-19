# 🚀 Alpaca Trading Course - Complete Tutorial Series

Kompletny kurs edukacyjny dotyczący algorytmicznego tradingu z wykorzystaniem API Alpaca.

## 📚 Lista Tutoriali

### Tutorial 02: Hello Alpaca
Pierwsze połączenie z API Alpaca i weryfikacja konta.
- 📁 Folder: `Alpaca02/`
- 🎯 Cel: Nauka podstawowej konfiguracji i połączenia z API

### Tutorial 04: Place Order
Składanie pierwszego zlecenia kupna/sprzedaży.
- 📁 Folder: `Alpaca04/`
- 🎯 Cel: Zrozumienie jak składać zlecenia market order

### Tutorial 05: Check Status
Sprawdzanie statusu złożonych zleceń.
- 📁 Folder: `Alpaca05/`
- 🎯 Cel: Monitorowanie zleceń i pozycji

### Tutorial 06: Main Loop Bot
Tworzenie pierwszego bota z pętlą główną.
- 📁 Folder: `Alpaca06/`
- 🎯 Cel: Budowa struktury działającego bota

### Tutorial 07: Calculate SMA
Obliczanie Simple Moving Average (SMA).
- 📁 Folder: `Alpaca07/`
- 🎯 Cel: Analiza techniczna - średnie kroczące

### Tutorial 08: Crossover Detector
Wykrywanie przecięć średnich kroczących (Golden Cross / Death Cross).
- 📁 Folder: `Alpaca08/`
- 🎯 Cel: Implementacja sygnałów tradingowych

### Tutorial 09: Crossover Bot v1
Pierwszy działający bot tradingowy oparty na przecięciach SMA.
- 📁 Folder: `Alpaca09/`
- 🎯 Cel: Połączenie analizy z automatycznym tradingiem

### Tutorial 10: Crossover Bot Final
Finalna wersja bota z pełną logiką wejścia i wyjścia.
- 📁 Folder: `Alpaca10/`
- 🎯 Cel: Kompletny system tradingowy

### Tutorial 11: Bracket Orders 🆕
Zaawansowane zarządzanie ryzykiem z wykorzystaniem bracket orders (Stop-Loss & Take-Profit).
- 📁 Folder: `Alpaca11/`
- 🎯 Cel: Automatyczna ochrona kapitału i zabezpieczenie zysków
- ✨ **Nowe funkcje**: 
  - Bracket Orders (OCO - One-Cancels-Other)
  - Automatyczny Stop-Loss (-2%)
  - Automatyczny Take-Profit (+5%)
  - "Set and Forget" approach

## 🎓 Filozofia Kursu

### Clarity Over Cleverness
- Priorytet: edukacja i zrozumienie
- Unikamy "magii" - preferujemy kod werbalny i jawny
- Jedna linia = jedna akcja

### Zasady Kodu
- ✅ Pełne, opisowe nazwy zmiennych
- ✅ Komentarze wyjaśniają "DLACZEGO", nie "CO"
- ✅ Każda funkcja robi jedną rzecz
- ✅ Wszystkie wywołania API w blokach try/except

## 🔒 Bezpieczeństwo

- ⚠️ **NIE commituj kluczy API!**
- Klucze przechowuj w `config.py` (dodany do `.gitignore`)
- Domyślnie używamy Paper Trading (bezpieczne testowanie)

## 📋 Wymagania

- Python 3.8+
- Konto Paper Trading w Alpaca ([Zarejestruj się](https://alpaca.markets/))
- Podstawowa znajomość Pythona

## 🚀 Szybki Start

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/TomaszCieslar/AlpacaTutorial.git
cd AlpacaTutorial
```

### 2. Przejdź do wybranego tutorialu

```bash
cd Alpaca11
```

### 3. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 4. Skonfiguruj klucze API

```bash
copy config.example.py config.py
```

Edytuj `config.py` i dodaj swoje klucze API.

### 5. Uruchom bota

```bash
python bracket_bot.py
```

## 📊 Struktura Projektu

```
AlpacaTutorial/
├── Alpaca02/           # Tutorial 02
├── Alpaca04/           # Tutorial 04
├── Alpaca05/           # Tutorial 05
├── Alpaca06/           # Tutorial 06
├── Alpaca07/           # Tutorial 07
├── Alpaca08/           # Tutorial 08
├── Alpaca09/           # Tutorial 09
├── Alpaca10/           # Tutorial 10
├── Alpaca11/           # Tutorial 11 (Bracket Orders)
├── .gitignore
├── README.md           # Ten plik
├── HOW_TO_PUBLISH.md   # Instrukcje publikacji
└── PUBLISH_GITHUB.md   # Przewodnik GitHub
```

## 🎯 Rekomendowana Ścieżka Nauki

1. **Zacznij od Tutorial 02** - Podstawy połączenia z API
2. **Przejdź kolejno** przez wszystkie tutoriale (02 → 11)
3. **Eksperymentuj** - modyfikuj parametry, testuj różne symbole
4. **Zawsze używaj Paper Trading** - nie ryzykuj prawdziwych pieniędzy podczas nauki

## ⚠️ Ważne Ostrzeżenia

- 🔴 **To tylko edukacja** - nie jest to porada finansowa
- 🔴 **Paper Trading Only** - używaj wyłącznie konta testowego
- 🔴 **Ryzyko** - handel na rynkach wiąże się z ryzykiem utraty kapitału
- 🔴 **Testuj dokładnie** - zanim pomyślisz o prawdziwym tradingu

## 🤝 Wkład w Projekt

Projekt edukacyjny otwarty na:
- Zgłaszanie problemów (issues)
- Sugestie ulepszeń
- Dzielenie się doświadczeniami edukacyjnymi

## 📄 Licencja

MIT License - Wolne użytkowanie do celów edukacyjnych

## 📞 Wsparcie

Masz pytania? Otwórz issue na GitHubie!

---

**Pamiętaj**: Nigdy nie handluj pieniędzmi, których nie możesz stracić. Zawsze najpierw testuj na paper trading! 📈🎓
