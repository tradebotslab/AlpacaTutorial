# 🚀 Alpaca Trading Course - Complete Tutorial Series

Kompletny kurs edukacyjny dotyczący algorytmicznego tradingu z wykorzystaniem API Alpaca. Kurs składa się z 30 lekcji, które prowadzą od podstaw (generowanie kluczy API) do zaawansowanych strategii (statistical arbitrage, pairs trading).

## 📚 Przegląd Kursu

Kurs jest podzielony na kilka sekcji tematycznych, które systematycznie budują wiedzę i umiejętności w zakresie algorytmicznego tradingu:

### 🔰 Sekcja 1: Podstawy (Lekcje 1-5)
**Fundamenty - Konfiguracja i pierwsze kroki**

- **Lesson 1: Generating API Keys in Alpaca** - Tworzenie konta Alpaca i generowanie kluczy API do paper trading
- **Lesson 2: "Hello, Alpaca!" - Connect & Check Your Account Status** - Pierwsze połączenie z API Alpaca i weryfikacja konta
- **Lesson 3: Fetching Market Data – Your First Candlestick** - Pobieranie historycznych danych OHLCV (Open, High, Low, Close, Volume)
- **Lesson 4: Place Market Order** - Składanie pierwszego zlecenia kupna/sprzedaży
- **Lesson 5: What Happened to My Order? – Checking Status & Positions** - Sprawdzanie statusu zleceń i pozycji

### 🔄 Sekcja 2: Budowa Bota (Lekcje 6-10)
**Struktura bota i podstawowe strategie**

- **Lesson 6: Anatomy of a Bot - The Main Loop** - Tworzenie głównej pętli bota umożliwiającej ciągłą pracę
- **Lesson 7: Simple Moving Average (SMA)** - Obliczanie średnich kroczących do analizy technicznej
- **Lesson 8: Moving Average Crossover Detector** - Wykrywanie przecięć średnich (Golden Cross / Death Cross)
- **Lesson 9: Simple Exit Logic – Selling on a Reversal Signal** - Implementacja logiki wyjścia z pozycji
- **Lesson 10: Moving Average Crossover Strategy - Complete Bot** - Kompletny, działający bot tradingowy

### 🛡️ Sekcja 3: Zarządzanie Ryzykiem (Lekcje 11-15)
**Ochrona kapitału i zarządzanie pozycjami**

- **Lesson 11: Bracket Orders - Stop-Loss & Take-Profit** - Automatyczna ochrona kapitału za pomocą bracket orders
- **Lesson 12: Take Your Profits! – Setting a Take-Profit Order** - Automatyczne zabezpieczanie zysków
- **Lesson 13: Never Risk Too Much – Calculating Position Size** - Dynamiczne obliczanie rozmiaru pozycji (fundament profesjonalnego zarządzania ryzykiem)
- **Lesson 14: Trailing Stop-Loss Bot** - Trailing stop-loss chroniący zyski podczas ruchu ceny w korzystnym kierunku
- **Lesson 15: Implementing a Trailing Stop-Loss in Code** - Zaawansowana implementacja trailing stop-loss od zera

### 📊 Sekcja 4: Zaawansowane Wskaźniki (Lekcje 16-20)
**Analiza techniczna i zaawansowane strategie**

- **Lesson 16: Relative Strength – Building an RSI-Based Bot** - Bot oparty na wskaźniku RSI (Relative Strength Index) do mean-reversion trading
- **Lesson 17: The Magic of Volatility – A Bollinger Bands® Bot** - Strategia "squeeze breakout" wykorzystująca Bollinger Bands
- **Lesson 18: The Power of Momentum – Implementing a MACD Strategy** - Bot wykorzystujący MACD (Moving Average Convergence Divergence) do wykrywania zmian momentum
- **Lesson 19: Signal Confirmation – Combining Two Indicators** - Łączenie wielu wskaźników dla potwierdzenia sygnałów
- **Lesson 20: The Bigger Picture – Analyzing Multiple Timeframes** - Analiza wielookresowa (Multi-Timeframe Analysis) - technika profesjonalnych traderów

### 🏗️ Sekcja 5: Produkcja i Profesjonalizm (Lekcje 21-25)
**Przygotowanie bota do produkcji**

- **Lesson 21: The Bot's "Black Box" – Logging Every Decision to a File** - Kompleksowe logowanie wszystkich decyzji tradingowych
- **Lesson 22: Stop Digging in the Code – Using an External Config File** - Separacja konfiguracji od kodu (profesjonalna praktyka)
- **Lesson 23: What If the Bot Restarts? – Managing Position State** - Zarządzanie stanem pozycji - bot z pamięcią przetrwa restart
- **Lesson 24: Stay Updated – Sending Real-Time Notifications to Discord** - Powiadomienia w czasie rzeczywistym przez Discord
- **Lesson 25: Making Your Bot Resilient – Handling API and Connection Errors** - Obsługa błędów i tworzenie odpornego bota gotowego do produkcji

### 🧪 Sekcja 6: Testowanie i Optymalizacja (Lekcje 26-28)
**Walidacja strategii i real-time data**

- **Lesson 26: Time Travel – The Basics of Backtesting Your Strategy** - Podstawy backtestingu strategii na danych historycznych
- **Lesson 27: Understanding Your Results – Analyzing a Backtest Report** - Analiza wyników backtestu jak profesjonalista (Annual Return, Max Drawdown, Sharpe Ratio)
- **Lesson 28: Faster Than HTTP – Streaming Real-Time Data with WebSockets** - Przejście z polling na WebSockets dla danych w czasie rzeczywistym

### 🚀 Sekcja 7: Deployment i Zaawansowane Strategie (Lekcje 29-30)
**Wdrożenie i strategie profesjonalne**

- **Lesson 29: Your Bot Online 24/7 – Deploying to a VPS Server** - Wdrożenie bota na serwer VPS dla pracy 24/7
- **Lesson 30: A Step Towards PRO – Statistical Arbitrage (Pairs Trading)** - Zaawansowana strategia market-neutral: pairs trading wykorzystująca cointegration

## 🎯 Cele Kursu

Po ukończeniu kursu będziesz potrafił:

- ✅ Skonfigurować środowisko deweloperskie i połączyć się z API Alpaca
- ✅ Pobierać i analizować dane rynkowe (OHLCV)
- ✅ Budować kompletne, działające boty tradingowe
- ✅ Implementować różne strategie tradingowe (trend-following, mean-reversion, momentum)
- ✅ Zarządzać ryzykiem profesjonalnie (position sizing, stop-loss, take-profit)
- ✅ Używać zaawansowanych wskaźników technicznych (SMA, RSI, MACD, Bollinger Bands)
- ✅ Łączyć wiele wskaźników i timeframe'ów dla lepszych sygnałów
- ✅ Tworzyć odporne boty gotowe do produkcji (error handling, logging, state management)
- ✅ Testować strategie na danych historycznych (backtesting)
- ✅ Wdrażać boty na serwerach VPS dla pracy 24/7
- ✅ Implementować zaawansowane strategie (pairs trading, statistical arbitrage)

## 📋 Wymagania

### Podstawowe Wymagania

- **Python 3.8+** (Python 3.10+ zalecany)
- **Konto Paper Trading w Alpaca** - [Zarejestruj się tutaj](https://alpaca.markets/)
- **Podstawowa znajomość Pythona** - zmienne, funkcje, pętle, listy
- **Podstawowa znajomość Git** (opcjonalnie, dla zarządzania kodem)

### Wymagane Biblioteki Python

Każda lekcja zawiera plik `requirements.txt` z wymaganymi zależnościami. Główne biblioteki używane w kursie:

- `alpaca-py` / `alpaca-trade-api` - Oficjalny SDK Alpaca
- `pandas` - Manipulacja danymi
- `numpy` - Obliczenia numeryczne
- `pandas-ta` - Wskaźniki techniczne
- `statsmodels` - Analiza statystyczna (dla pairs trading)
- `backtesting` - Backtesting strategii
- `requests` - HTTP requests (dla Discord webhooks)

## 🚀 Szybki Start

### 1. Sklonuj Repozytorium

```bash
git clone https://github.com/TomaszCieslar/AlpacaTutorial.git
cd AlpacaTutorial
```

### 2. Rozpocznij od Lekcji 1

```bash
cd Alpaca01
```

### 3. Zainstaluj Zależności

```bash
pip install -r requirements.txt
```

### 4. Skonfiguruj Klucze API

```bash
# Skopiuj przykładowy plik konfiguracyjny
cp config.example.py config.py

# Edytuj config.py i dodaj swoje klucze API z Alpaca
# ⚠️ NIGDY nie commituj config.py do Git!
```

### 5. Uruchom Przykładowy Kod

```bash
# Dla lekcji 2:
python hello_alpaca.py

# Dla lekcji 3:
python fetch_data.py

# Dla lekcji 4:
python place_order.py

# itd...
```

## 📁 Struktura Projektu

```
AlpacaTutorial/
├── Alpaca01/              # Lekcja 1: Generowanie kluczy API
├── Alpaca02/              # Lekcja 2: Połączenie z API
├── Alpaca03/              # Lekcja 3: Pobieranie danych rynkowych
├── Alpaca04/              # Lekcja 4: Składanie zleceń
├── Alpaca05/              # Lekcja 5: Sprawdzanie statusu
├── Alpaca06/              # Lekcja 6: Główna pętla bota
├── Alpaca07/              # Lekcja 7: Obliczanie SMA
├── Alpaca08/              # Lekcja 8: Wykrywanie crossover
├── Alpaca09/              # Lekcja 9: Logika wyjścia
├── Alpaca10/              # Lekcja 10: Kompletny bot
├── Alpaca11/              # Lekcja 11: Bracket orders
├── Alpaca12/              # Lekcja 12: Take-profit
├── Alpaca13/              # Lekcja 13: Position sizing
├── Alpaca14/              # Lekcja 14: Trailing stop
├── Alpaca15/              # Lekcja 15: Manual trailing stop
├── Alpaca16/              # Lekcja 16: RSI bot
├── Alpaca17/              # Lekcja 17: Bollinger Bands
├── Alpaca18/              # Lekcja 18: MACD strategy
├── Alpaca19/              # Lekcja 19: Signal confirmation
├── Alpaca20/              # Lekcja 20: Multi-timeframe
├── Alpaca21/              # Lekcja 21: Logging
├── Alpaca22/              # Lekcja 22: External config
├── Alpaca23/              # Lekcja 23: State management
├── Alpaca24/              # Lekcja 24: Discord notifications
├── Alpaca25/              # Lekcja 25: Error handling
├── Alpaca26/              # Lekcja 26: Backtesting
├── Alpaca27/              # Lekcja 27: Backtest analysis
├── Alpaca28/              # Lekcja 28: WebSockets
├── Alpaca29/              # Lekcja 29: VPS deployment
├── Alpaca30/              # Lekcja 30: Pairs trading
├── Instructions/          # Szczegółowe instrukcje dla każdej lekcji
├── README.md              # Ten plik
└── templateReadmy.md      # Szablon dla dokumentacji lekcji
```

## 🎓 Filozofia Kursu

### Clarity Over Cleverness

Kurs priorytetyzuje **jasność nad sprytem**:

- ✅ **Pełne, opisowe nazwy zmiennych** - `take_profit_price` zamiast `tp`
- ✅ **Komentarze wyjaśniają "DLACZEGO"** - nie tylko "CO"
- ✅ **Jedna linia = jedna akcja** - unikamy złożonych, zagnieżdżonych wyrażeń
- ✅ **Każda funkcja robi jedną rzecz** - zasada Single Responsibility
- ✅ **Brak "magii"** - preferujemy kod werbalny i jawny

### Zasady Kodu Edukacyjnego

- **Edukacja przed optymalizacją** - kod jest czytelny, niekoniecznie najszybszy
- **Explicit over implicit** - wszystko jest wyraźnie napisane
- **Error handling** - wszystkie wywołania API w blokach try/except
- **Paper Trading First** - zawsze zaczynamy od bezpiecznego testowania

## 🔒 Bezpieczeństwo

### ⚠️ Krytyczne Zasady

1. **NIGDY nie commituj kluczy API!**
   - Plik `config.py` jest w `.gitignore`
   - Używaj `config.example.py` jako szablonu
   - Nigdy nie udostępniaj kluczy publicznie

2. **Zawsze używaj Paper Trading podczas nauki**
   - Domyślnie wszystkie przykłady używają `https://paper-api.alpaca.markets`
   - Testuj strategie bez ryzyka finansowego
   - Przejdź na live trading dopiero po dokładnym przetestowaniu

3. **Chroń swoje klucze API**
   - Traktuj je jak hasła
   - Rotuj klucze jeśli podejrzewasz kompromitację
   - Używaj osobnych kluczy dla paper i live trading

## 📊 Rekomendowana Ścieżka Nauki

### Dla Początkujących

1. **Zacznij od Lekcji 1-5** - Podstawy konfiguracji i pierwszych operacji
2. **Przejdź przez Lekcje 6-10** - Budowa pierwszego działającego bota
3. **Skoncentruj się na Lekcjach 11-15** - Zarządzanie ryzykiem jest kluczowe
4. **Eksperymentuj** - Modyfikuj parametry, testuj różne symbole
5. **Zawsze używaj Paper Trading** - Nie ryzykuj prawdziwych pieniędzy podczas nauki

### Dla Zaawansowanych

- **Lekcje 16-20** - Zaawansowane wskaźniki i strategie
- **Lekcje 21-25** - Przygotowanie do produkcji
- **Lekcje 26-28** - Testowanie i optymalizacja
- **Lekcje 29-30** - Deployment i zaawansowane strategie

## 🎯 Kluczowe Koncepcje Nauczane w Kursie

### Podstawy Tradingu

- **Market Orders** - Podstawowe zlecenia kupna/sprzedaży
- **OHLCV Data** - Dane świecowe (Open, High, Low, Close, Volume)
- **Position Management** - Zarządzanie pozycjami
- **Order Status** - Śledzenie statusu zleceń

### Analiza Techniczna

- **Simple Moving Average (SMA)** - Średnie kroczące
- **Relative Strength Index (RSI)** - Wskaźnik siły względnej
- **MACD** - Moving Average Convergence Divergence
- **Bollinger Bands** - Pasy Bollingera do pomiaru zmienności
- **Crossover Signals** - Sygnały przecięcia (Golden Cross, Death Cross)

### Zarządzanie Ryzykiem

- **Position Sizing** - Dynamiczne obliczanie rozmiaru pozycji
- **Stop-Loss Orders** - Automatyczna ochrona przed stratami
- **Take-Profit Orders** - Automatyczne zabezpieczanie zysków
- **Bracket Orders** - Kombinacja entry, stop-loss i take-profit
- **Trailing Stops** - Stop-loss podążający za ceną

### Zaawansowane Techniki

- **Multi-Timeframe Analysis** - Analiza wielookresowa
- **Signal Confirmation** - Potwierdzanie sygnałów wieloma wskaźnikami
- **Mean-Reversion Trading** - Strategie powrotu do średniej
- **Trend-Following** - Strategie podążania za trendem
- **Pairs Trading** - Statystyczny arbitraż (market-neutral)

### Produkcja i Deployment

- **Error Handling** - Obsługa błędów i odporność bota
- **Logging** - Kompleksowe logowanie decyzji
- **State Management** - Zarządzanie stanem pozycji
- **External Configuration** - Separacja konfiguracji od kodu
- **Discord Notifications** - Powiadomienia w czasie rzeczywistym
- **VPS Deployment** - Wdrożenie na serwerze dla pracy 24/7
- **Backtesting** - Testowanie strategii na danych historycznych
- **WebSockets** - Streaming danych w czasie rzeczywistym

## ⚠️ Ważne Ostrzeżenia

### 🔴 To Tylko Edukacja

- **Nie jest to porada finansowa** - Kurs ma charakter wyłącznie edukacyjny
- **Paper Trading Only** - Używaj wyłącznie konta testowego podczas nauki
- **Ryzyko** - Handel na rynkach wiąże się z ryzykiem utraty kapitału
- **Testuj dokładnie** - Zanim pomyślisz o prawdziwym tradingu, przetestuj wszystko w paper trading

### 🟡 Zasady Bezpieczeństwa

- **Nigdy nie handluj pieniędzmi, których nie możesz stracić**
- **Zawsze testuj w paper trading przed live trading**
- **Rozumiej strategię przed wdrożeniem**
- **Monitoruj swoje strategie regularnie**
- **Używaj właściwych praktyk bezpieczeństwa**
- **Rób kopie zapasowe konfiguracji**

## 📚 Dodatkowe Zasoby

### Dokumentacja Alpaca

- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [Alpaca Python SDK](https://github.com/alpacahq/alpaca-trade-api-python)
- [Alpaca Market Data API](https://alpaca.markets/docs/api-documentation/market-data-api/)

### Wsparcie

- [Alpaca Support Center](https://alpaca.markets/support)
- [Alpaca Status Page](https://status.alpaca.markets/)
- [GitHub Issues](https://github.com/TomaszCieslar/AlpacaTutorial/issues) - Zgłaszaj problemy i pytania

## 🤝 Wkład w Projekt

Projekt edukacyjny otwarty na:

- ✅ Zgłaszanie problemów (issues)
- ✅ Sugestie ulepszeń
- ✅ Dzielenie się doświadczeniami edukacyjnymi
- ✅ Pull requests z poprawkami

## 📄 Licencja

MIT License - Wolne użytkowanie do celów edukacyjnych

## 🎓 Podsumowanie

Ten kurs prowadzi Cię od zera do zaawansowanego poziomu w algorytmicznym tradingu. Po ukończeniu wszystkich 30 lekcji będziesz posiadał:

- ✅ Kompletny, odporny bot tradingowy działający 24/7
- ✅ Wiedzę o wielu strategiach tradingowych (directional i market-neutral)
- ✅ Umiejętności zarządzania ryzykiem i position sizing
- ✅ Możliwość backtestowania strategii
- ✅ Umiejętność wdrożenia bota na serwerze VPS
- ✅ Zaawansowane strategie statystycznego arbitrażu

**"Risk comes from not knowing what you're doing." - Warren Buffett**

Zacznij od Lekcji 1 i krok po kroku buduj swoją wiedzę. Pamiętaj: zawsze testuj w paper trading i nigdy nie ryzykuj więcej, niż możesz stracić.

---

**Happy Trading! 📈🎓**

*Alpaca Trading Course - Complete Tutorial Series*  
*30 lekcji od podstaw do zaawansowanych strategii*
