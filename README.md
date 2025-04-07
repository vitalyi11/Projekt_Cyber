Cyberbezpieczeństwo Projekt - Narzędzie diagnostyczne sieci

Narzędzie diagnostyczne sieci
Ta aplikacja udostępnia graficzny interfejs dla różnych narzędzi diagnostycznych sieci, umożliwiając użytkownikom monitorowanie sieci WiFi, śledzenie tras sieciowych oraz przeglądanie aktywnych połączeń sieciowych.

Funkcje
Skaner WiFi
Skanuje i wyświetla dostępne sieci WiFi w twojej okolicy
Pokazuje szczegółowe informacje, w tym:
SSID (nazwa sieci)
Numer kanału
Częstotliwość (2.4 GHz lub 5 GHz)
Siła sygnału (w dBm)
Automatycznie odświeża co 10 sekund
Wspiera ręczne skanowanie po kliknięciu przycisku
Traceroute
Śledzi trasę, którą pakiety pokonują do określonego celu sieciowego
Pokazuje każdy przeskok na ścieżce sieciowej
Kompatybilny z platformami Windows, Linux i macOS
Wyświetla wyniki w czasie rzeczywistym
Netstat
Wyświetla aktywne połączenia sieciowe w systemie
Pokazuje nasłuchujące porty i ustanowione połączenia
Dostosowuje komendy w zależności od systemu operacyjnego
Generuje szczegółowe statystyki sieciowe
Wymagania
Python 3.x
PyQt5
Wsparcie systemu operacyjnego dla natywnych komend sieciowych:
Windows: netsh, tracert, netstat
Linux: traceroute, netstat lub ss
macOS: traceroute, netstat

Użytkowanie
Skaner WiFi
Zakładka skanera WiFi wyświetla tabelę dostępnych sieci. Kliknij "Skanuj sieci WiFi", aby ręcznie odświeżyć listę.

Traceroute
Wprowadź adres docelowy (np. google.com, 8.8.8.8)
Kliknij "Uruchom Traceroute" lub naciśnij Enter
Zobacz informacje o trasie w oknie wyjściowym
Netstat
Kliknij "Wyświetl Netstat", aby zobaczyć aktualne informacje o połączeniach sieciowych.

Szczegóły techniczne
Aplikacja wykorzystuje:

PyQt5 do interfejsu użytkownika
QProcess do asynchronicznego wykonywania poleceń
Komendy specyficzne dla danej platformy do diagnostyki sieci
Wyrażenia regularne do analizy wyjścia komend