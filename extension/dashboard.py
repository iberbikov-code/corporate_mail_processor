import os
from pathlib import Path
import streamlit as st
import pandas as pd

# Настройка страницы
st.set_page_config(page_title="Аналитика IT-Отдела", page_icon="📊", layout="wide")
st.title("📊 Автоматизированная система обработки IT-обращений")
st.markdown("Интерактивный отчет по результатам работы лексического классификатора.")

# Путь к выходной папке
base_dir = Path(__file__).resolve().parent.parent
output_dir = base_dir / "output"

@st.cache_data(ttl=30)
def load_data():
    """Считывает результаты работы классификатора из папки output."""
    if not output_dir.exists():
        return None
    
    data = []
    for category_dir in output_dir.iterdir():
        if category_dir.is_dir():
            count = len(list(category_dir.glob("*")))
            data.append({"Категория": category_dir.name, "Количество писем": count})
    return pd.DataFrame(data)

df = load_data()

if df is None or df.empty:
    st.warning("Нет данных для анализа. Сначала запустите основную маршрутизацию писем.")
else:
    # Метрики
    total_emails = df["Количество писем"].sum()
    critical_count = df.loc[df["Категория"] == "critical_incidents", "Количество писем"].sum() if "critical_incidents" in df["Категория"].values else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Всего обработано", int(total_emails))
    col2.metric("Критические сбои (SLA 15м)", int(critical_count), delta_color="inverse")
    col3.metric("Аномалии в карантине", int(df.loc[df["Категория"] == "quarantine", "Количество писем"].sum() if "quarantine" in df["Категория"].values else 0))

    st.markdown("---")
    
    # Графики
    st.subheader("Распределение нагрузки по категориям")
    st.bar_chart(df.set_index("Категория"))

    st.markdown("---")
    st.subheader("🚨 Внимание: Критические инциденты")
    critical_dir = output_dir / "critical_incidents"
    if critical_dir.exists() and any(critical_dir.iterdir()):
        for file_path in critical_dir.iterdir():
            if file_path.is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        snippet = f.read(300)
                    with st.expander(f"Отчет: {file_path.name}"):
                        st.text(snippet)
                except Exception:
                    st.error(f"Невозможно прочитать файл: {file_path.name}")
    else:
        st.success("Отличные новости! Критических инцидентов в данный момент нет.")