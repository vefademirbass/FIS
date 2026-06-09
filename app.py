import streamlit as st
import pandas as pd
import plotly.express as px
import time
import plotly.graph_objects as go
# --- SAYFA AYARLARI ---
# Sekmeli tasarımda ekranı daha iyi kullanmak için layout'u "wide" (geniş) yaptık
st.set_page_config(page_title="AFAD Decision Support", page_icon="🚨", layout="wide")

# --- BAŞLIK VE AÇIKLAMA ---
st.title("Multi-Hazard EOC Prioritization System")
st.markdown("**Developed by:** Hacettepe University Industrial Engineering (Berfin, Vefa, Ece, Betül)")
st.divider()

# --- SEKMELERİ (TABS) OLUŞTURMA ---
tab1, tab2, tab3 = st.tabs([
    "🌍 Historical Hazard Map", 
    "⚙️ DSS Simulation Panel", 
    "📊 Algorithm Architecture"
])

# ==========================================
# SEKME 1: TARİHSEL AFET HARİTASI (GENİŞLETİLMİŞ VERİ SETİ)
# ==========================================
with tab1:
    st.subheader("National Hazard Risk & Historical Data Map")
    
    map_layer = st.radio(
        "Select Hazard Layer to Visualize:", 
        ["Base Map", "Earthquake (Historical)", "Wildfire (Historical)", "Flood (Historical)"], 
        horizontal=True
    )

    center_lat, center_lon = 39.0, 35.0

    if map_layer == "Earthquake (Historical)":
        df_eq = pd.DataFrame({
            "Location": [
                "Gölcük (1999)", "Düzce (1999)", "Van (2011)", "Elazığ (2020)", "İzmir (2020)", 
                "K.Maraş (2023)", "Hatay (2023)", "Erzincan (1939)", "Adana/Ceyhan (1998)", 
                "Bingöl (2003)", "Kütahya/Simav (2011)", "Çanakkale/Ayvacık (2017)", "Malatya (2024)",
                "Erbaa/Tokat (1942)", "Tosya/Kastamonu (1943)", "Bolu/Gerede (1944)", "Yenice/Çanakkale (1953)",
                "Varto/Muş (1966)", "Bingöl (1971)", "Çaldıran/Van (1976)", "Horasan/Erzurum (1983)",
                "Erzincan (1992)", "Dinar/Afyon (1995)", "Bodrum/Muğla (2017)", "Yalova (1995)"
            ],
            "lat": [40.71, 40.84, 38.66, 38.40, 37.89, 37.28, 36.20, 39.75, 36.98, 39.00, 39.09, 39.60, 38.09,
                    40.66, 41.01, 40.80, 39.92, 39.17, 39.00, 39.14, 40.04, 39.71, 38.06, 36.93, 40.65],
            "lon": [29.81, 31.15, 43.32, 39.31, 26.79, 37.04, 36.16, 39.49, 35.81, 40.48, 28.98, 26.40, 37.88,
                    36.56, 34.04, 32.19, 27.25, 41.45, 40.48, 43.91, 42.16, 39.62, 30.15, 27.53, 29.27],
            "Magnitude": [7.4, 7.2, 7.2, 6.8, 6.6, 7.8, 6.4, 7.9, 6.2, 6.4, 5.9, 5.3, 5.9,
                          7.0, 7.2, 7.2, 7.2, 6.9, 6.8, 7.5, 6.9, 6.8, 6.1, 6.6, 5.5]
        })
        df_eq["Size"] = df_eq["Magnitude"] ** 2.5 
        fig = px.scatter_mapbox(
            df_eq, lat="lat", lon="lon", size="Size", color="Magnitude",
            color_continuous_scale=["#FF9999", "#E60000", "#8B0000"],
            size_max=25, zoom=4.5, hover_name="Location",
            hover_data={"lat": False, "lon": False, "Size": False, "Magnitude": True},
            center=dict(lat=center_lat, lon=center_lon), mapbox_style="carto-positron"
        )

    elif map_layer == "Wildfire (Historical)":
        df_fire = pd.DataFrame({
            "Location": [
                # Birinci Derece Risk (Akdeniz & Ege)
                "Manavgat/Antalya (2021)", "Marmaris/Muğla (2021)", "Bodrum/Muğla (2021)", 
                "Serik/Antalya (2008)", "Milas/Muğla (2021)", "Köyceğiz/Muğla (2021)", 
                "Belen/Hatay (2020)", "Gülnar/Mersin (2022)", "Kumluca/Antalya (2022)", 
                "Karşıyaka/İzmir (2024)", "Menderes/İzmir (2017)",
                # Marmara ve İç Anadolu Geçişleri
                "Merkez/Çanakkale (2023)", "Eceabat/Çanakkale (2024)", "Mudurnu/Bolu (2022)", 
                "Kızılcahamam/Ankara (2020)", "Keles/Bursa (2022)", "Gelibolu/Çanakkale (1994)",
                # Karadeniz Lodos Yangınları
                "Sürmene/Trabzon (2017)", "Vezirköprü/Samsun (2020)", "Ardeşen/Rize (2021)",
                # Güneydoğu Tarım/Anız Yangınları
                "Mazıdağı/Mardin (2024)", "Bismil/Diyarbakır (2024)"
            ],
            "lat": [36.78, 36.85, 37.03, 36.91, 37.31, 36.96, 36.48, 36.33, 36.37, 38.45, 38.25,
                    40.15, 40.18, 40.46, 40.47, 39.91, 40.41,
                    40.91, 41.14, 41.19,
                    37.50, 37.83],
            "lon": [31.44, 28.27, 27.43, 31.10, 27.78, 28.69, 36.20, 33.39, 30.28, 27.10, 27.13,
                    26.40, 26.35, 31.21, 32.65, 29.23, 26.67,
                    40.11, 35.45, 40.98,
                    40.48, 39.87],
            "Burned_Hectares": [60000, 13000, 11000, 16000, 8000, 11000, 400, 1500, 1000, 1500, 1000,
                                4000, 2500, 500, 300, 800, 4000,
                                250, 400, 150,
                                15000, 8000]
        })
        fig = px.scatter_mapbox(
            df_fire, lat="lat", lon="lon", size="Burned_Hectares", color="Burned_Hectares",
            color_continuous_scale=["#FFD700", "#FF6347", "#8B0000"],
            size_max=35, zoom=4.5, hover_name="Location",
            hover_data={"lat": False, "lon": False, "Burned_Hectares": True},
            center=dict(lat=center_lat, lon=center_lon), mapbox_style="carto-positron"
        )
        

    elif map_layer == "Flood (Historical)":
        df_flood = pd.DataFrame({
            "Location": [
                "Bozkurt/Kastamonu (2021)", "Ayancık/Sinop (2021)", "Dereli/Giresun (2020)", 
                "Şanlıurfa (2023)", "Bartın (1998)", "Hopa/Artvin (2015)", "Araklı/Trabzon (2019)", 
                "Meriç/Edirne (2018)", "Çayeli/Rize (2020)", "Mamak/Ankara (2018)", "Akçakoca/Düzce (2019)",
                "Ayamama/İstanbul (2009)", "Terme/Samsun (2019)", "Fatsa/Ordu (2018)", "Arhavi/Artvin (2021)",
                "Kumluca/Antalya (2022)", "Esenyurt/İstanbul (2020)", "Gökçebey/Zonguldak (2023)", 
                "Güneyce/Rize (2010)", "Devrek/Zonguldak (2023)", "Bismil/Diyarbakır (2006)", "Erciş/Van (2006)"
            ],
            "lat": [41.95, 41.94, 40.73, 37.16, 41.63, 41.39, 40.93, 41.67, 41.09, 39.93, 41.08,
                    41.01, 41.20, 41.02, 41.34, 36.37, 41.03, 41.30, 40.83, 41.22, 37.83, 39.02],
            "lon": [34.00, 34.58, 38.44, 38.79, 32.33, 41.43, 40.05, 26.56, 40.72, 32.92, 31.11,
                    28.82, 36.97, 37.50, 41.30, 30.28, 28.67, 32.09, 40.48, 31.95, 39.87, 43.35],
            "Impact_Level": [
                "Catastrophic", "Severe", "Severe", "High", "Catastrophic", "Severe", "Severe", 
                "High", "High", "High", "Severe", "Catastrophic", "Severe", "High", "Severe",
                "High", "High", "Severe", "Severe", "Severe", "High", "High"
            ],
            "Severity_Score": [10, 9, 9, 8, 10, 9, 9, 7, 8, 7, 9, 10, 9, 8, 9, 7, 7, 9, 9, 9, 8, 8]
        })
        fig = px.scatter_mapbox(
            df_flood, lat="lat", lon="lon", size="Severity_Score", color="Severity_Score",
            color_continuous_scale=["#87CEFA", "#4169E1", "#00008B"],
            size_max=20, zoom=4.5, hover_name="Location",
            hover_data={"lat": False, "lon": False, "Severity_Score": False, "Impact_Level": True},
            center=dict(lat=center_lat, lon=center_lon), mapbox_style="carto-positron"
        )

    else:
        fig = px.scatter_mapbox(lat=[center_lat], lon=[center_lon], zoom=4.5, mapbox_style="carto-positron")

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# SEKME 2: SIMULASYON VE HESAPLAMA EKRANI (İnteraktif Versiyon)
# ==========================================
with tab2:
    st.subheader("Field Data Input & Prioritization Engine")
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("#### 📥 Enter Field Parameters")
        hazard_type = st.selectbox("Select Disaster Type:", ["Earthquake", "Flood", "Wildfire"])
        severity = st.slider("Damage Severity (0-10)", 0.0, 10.0, 5.0, step=0.1)
        accessibility = st.slider("Accessibility (10=Blocked, 0=Clear)", 0.0, 10.0, 5.0, step=0.1)
        population = st.slider("Population Exposure (0-10)", 0.0, 10.0, 5.0, step=0.1)
        
        # Radar Grafiği Çizimi
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[severity, accessibility, population, severity], # Poligonu kapatmak için sonuna ilk veriyi ekliyoruz
            theta=['Severity', 'Accessibility', 'Population', 'Severity'],
            fill='toself',
            line_color='#FF4B4B' if hazard_type == "Earthquake" else ('#0068C9' if hazard_type == "Flood" else '#FFA500')
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=300
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col2:
        st.markdown(f"#### ⚙️ Active Scenario: :red[{hazard_type}]")
        st.write("Awaiting priority calculation based on the Weighted Fuzzy Inference System...")
        
        if st.button("🚀 EXECUTE WEIGHTED FIS", use_container_width=True):
            
            # --- 1. ŞOV KISMI: Yükleme Animasyonu ---
            with st.spinner('⏳ Processing field data & applying fuzzy logic rules...'):
                time.sleep(1.5) # Jüride beklenti yaratmak için 1.5 saniye simülasyon beklemesi
            
            # --- 2. HESAPLAMA ---
            if hazard_type == "Earthquake":
                base_score = (severity * 0.45) + (accessibility * 0.30) + (population * 0.25)
            elif hazard_type == "Flood":
                base_score = (severity * 0.35) + (accessibility * 0.40) + (population * 0.25)
            else: 
                base_score = (severity * 0.40) + (accessibility * 0.20) + (population * 0.40)
                
            final_score = base_score * 10 
            
            # --- 3. GÖRSEL SONUÇLAR ---
            st.divider()
            # --- HİKAYELEŞTİRME MOTORU (NARRATIVE ENGINE) ---
            st.markdown("#### 📖 Scenario Interpretation")
            
            # Severity hikayesi
            if severity >= 8:
                sev_text = f"**Damage Severity ({severity}):** The simulation reflects a catastrophic structural failure, comparable to major historical events (Mw 7.0+). The system assumes widespread non-engineered building collapse."
            elif severity >= 5:
                sev_text = f"**Damage Severity ({severity}):** Moderate damage detected. Critical structural integrity is maintained, but significant local repairs are required."
            else:
                sev_text = f"**Damage Severity ({severity}):** Minor surface damage. The infrastructure is resilient to the current hazard intensity."
            
            # Accessibility hikayesi
            if accessibility >= 7:
                acc_text = f"**Accessibility ({accessibility}):** Logistical bottleneck! Main arteries are compromised by debris or environmental factors (snow/water), requiring aerial or maritime intervention."
            else:
                acc_text = f"**Accessibility ({accessibility}):** Transport routes remain operational, allowing for standard ground-based emergency vehicle movement."
                
            # Population hikayesi
            if population >= 8:
                pop_text = f"**Population Exposure ({population}):** High-density urban zone. The incident occurred in a high-occupancy period, putting approximately 100k+ lives at immediate risk."
            else:
                pop_text = f"**Population Exposure ({population}):** Low-to-moderate density zone. The risk profile is localized to peripheral infrastructure."

            # Hikayeleri ekrana basma
            st.info(f"{sev_text}\n\n{acc_text}\n\n{pop_text}")
            
            # Metrik ve Skor Çubuğu
            st.metric(label="Calculated Priority Score", value=f"{final_score:.2f} / 100")
            st.progress(int(final_score) / 100) # 0 ile 1 arası değer alır
            
            # --- 4. GÖRSEL LOJİSTİK VE KAYNAK ATAMA ---
            st.markdown("#### 🚁 Recommended Resource Deployment")
            if final_score >= 75:
                st.error("🚨 **ACTION:** IMMEDIATE DEPLOYMENT REQUIRED! (Very High Priority)")
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("USAR Teams", "15 Units", "High Demand")
                col_b.metric("Ambulances", "40 Units", "Critical")
                col_c.metric("Air Support", "5 Helis", "Clearance Needed")
                
            elif final_score >= 50:
                st.warning("⚠️ **ACTION:** STANDBY FOR DISPATCH (Medium-High Priority)")
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("USAR Teams", "5 Units", "Standby")
                col_b.metric("Ambulances", "15 Units", "Ready")
                col_c.metric("Air Support", "1 Heli", "Monitoring")
                
            else:
                st.info("ℹ️ **ACTION:** MONITOR SITUATION (Low-Medium Priority)")
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("USAR Teams", "1 Unit", "Local Only")
                col_b.metric("Ambulances", "3 Units", "Routine")
                col_c.metric("Air Support", "0", "Not Required")
# ==========================================
# SEKME 3: ALGORİTMA VE SİSTEM MANTIGI
# ==========================================
with tab3:
    st.subheader("🧠 System Architecture & Rule Weights")
    st.markdown("""
    This Decision Support System (DSS) evaluates emergency scenarios using a **Multi-Hazard Weighted Fuzzy Inference System**. 
    Unlike static formulas, the system dynamically shifts the importance of field parameters based on the specific nature of the disaster.
    """)
    
    st.markdown("#### Dynamically Applied Weights ($w_r$)")
    weight_data = pd.DataFrame({
        "Parameter": ["Damage Severity", "Accessibility Limitation", "Population Exposure"],
        "Earthquake Weights": ["45%", "30%", "25%"],
        "Flood Weights": ["35%", "40%", "25%"],
        "Wildfire Weights": ["40%", "20%", "40%"]
    })
    
    st.table(weight_data)
    st.caption("Note: During an Earthquake, structural severity dominates the prioritization logic. In contrast, Flood scenarios place heavier emphasis on accessibility constraints due to submerged infrastructure.")