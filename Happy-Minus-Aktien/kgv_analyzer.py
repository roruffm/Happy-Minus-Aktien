#!/usr/bin/env python3
"""
KGV-Analyzer: Identifiziert unterbewertete Aktien basierend auf dem Kurs-Gewinn-Verhältnis (KGV).
Aktualisiert alle 10 Minuten und speichert die Ergebnisse in einer CSV-Datei.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# Liste der zu analysierenden Aktien (DAX, MDAX, S&P 500, etc.)
# Kann durch eine API oder manuelle Liste ersetzt werden
TICKERS = [
    # DAX
    "SAP.DE", "BMW.DE", "AIR.DE", "BAS.DE", "BAYN.DE", "DB1.DE", "DPW.DE", 
    "DTE.DE", "FRE.DE", "HEI.DE", "IFX.DE", "LIN.DE", "MRK.DE", "PAH3.DE", 
    "PUM.DE", "RWE.DE", "SZG.DE", "VNA.DE", "VOW3.DE", "ZAL.DE",
    # MDAX (Beispiele)
    "ALV.DE", "CBK.DE", "DBK.DE", "DPAG.DE", "FME.DE", "HEN3.DE", 
    "MAN.DE", "PZU.DE", "SDF.DE", "TUI1.DE",
    # S&P 500 (Beispiele)
    "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "BRK-B", "JNJ", "JPM", "V",
]

# Schwellenwert für KGV (unterbewertet, wenn KGV < THRESHOLD)
KGV_THRESHOLD = 15

# Mindest-EPS (Gewinn pro Aktie), um Aktien mit negativem Gewinn auszuschließen
MIN_EPS = 0.1

# Ausgabedatei
OUTPUT_FILE = "unterbewertete_aktien.csv"


def get_stock_data(ticker: str) -> dict:
    """
    Ruft aktuelle Daten für eine Aktie über Yahoo Finance ab.
    
    Args:
        ticker (str): Aktien-Symbol (z. B. "SAP.DE")
    
    Returns:
        dict: Enthält Kurs, KGV, EPS, Dividendenrendite und Name
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        current_price = info.get("currentPrice", None)
        pe_ratio = info.get("trailingPE", None)  # KGV
        eps = info.get("trailingEps", None)
        dividend_yield = info.get("dividendYield", 0)
        long_name = info.get("longName", ticker)
        
        return {
            "Ticker": ticker,
            "Name": long_name,
            "Kurs": current_price,
            "KGV": pe_ratio,
            "EPS": eps,
            "Dividendenrendite": dividend_yield,
        }
    except Exception as e:
        print(f"Fehler bei {ticker}: {e}")
        return None


def filter_undervalued_stocks(stock_data: list) -> pd.DataFrame:
    """
    Filtert unterbewertete Aktien basierend auf KGV und EPS.
    
    Args:
        stock_data (list): Liste mit Aktien-Daten
    
    Returns:
        pd.DataFrame: DataFrame mit unterbewerteten Aktien
    """
    df = pd.DataFrame(stock_data)
    
    # Filter: KGV < THRESHOLD und EPS > MIN_EPS
    undervalued_df = df[
        (df["KGV"].notna()) & 
        (df["KGV"] < KGV_THRESHOLD) & 
        (df["EPS"].notna()) & 
        (df["EPS"] > MIN_EPS)
    ].copy()
    
    # Sortieren nach KGV (niedrigste zuerst)
    undervalued_df = undervalued_df.sort_values(by="KGV")
    
    # Zeitstempel hinzufügen
    undervalued_df["Zeitstempel"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return undervalued_df


def save_results(df: pd.DataFrame, filename: str = OUTPUT_FILE) -> None:
    """
    Speichert die Ergebnisse in einer CSV-Datei.
    
    Args:
        df (pd.DataFrame): DataFrame mit den Ergebnissen
        filename (str): Dateiname
    """
    df.to_csv(filename, index=False)
    print(f"Ergebnisse in {filename} gespeichert.")


def get_undervalued_stocks() -> pd.DataFrame:
    """
    Hauptfunktion: Ruft Daten für alle Aktien ab und filtert unterbewertete.
    
    Returns:
        pd.DataFrame: DataFrame mit unterbewerteten Aktien
    """
    stock_data = []
    
    for ticker in TICKERS:
        data = get_stock_data(ticker)
        if data:
            stock_data.append(data)
    
    undervalued_df = filter_undervalued_stocks(stock_data)
    return undervalued_df


def main():
    """Hauptfunktion für die Ausführung."""
    print(f"Starte KGV-Analyse um {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    undervalued_df = get_undervalued_stocks()
    
    if undervalued_df.empty:
        print("Keine unterbewerteten Aktien gefunden.")
    else:
        print(f"Gefunden: {len(undervalued_df)} unterbewertete Aktien")
        print(undervalued_df.to_string(index=False))
        
        # Speichern
        save_results(undervalued_df)
    
    print(f"Analyse abgeschlossen um {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


if __name__ == "__main__":
    main()