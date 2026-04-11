import pandas as pd
import numpy as np
import os

def generate_social_impact_data():
    """
    Generates Barcelona 2026 data focused on Urban Equity and Sustainability.
    Analyzes the 'Trade-off' between Green Mobility and Housing Affordability.
    """
    os.makedirs('data', exist_ok=True)
    
    # Districts with Social and Environmental context
    # prestige here becomes the 'Economic Power' base for the simulation
    districts = [
        {"name": "Eixample", "price_m2": 26.5, "vulnerability": 2, "lat": 41.3888, "lon": 2.1627},
        {"name": "Ciutat Vella", "price_m2": 25.0, "vulnerability": 7, "lat": 41.3800, "lon": 2.1700},
        {"name": "Sarrià-St. Gervasi", "price_m2": 24.0, "vulnerability": 1, "lat": 41.4000, "lon": 2.1200},
        {"name": "Gràcia", "price_m2": 23.5, "vulnerability": 4, "lat": 41.4029, "lon": 2.1534},
        {"name": "Sant Martí", "price_m2": 23.0, "vulnerability": 5, "lat": 41.4000, "lon": 2.2000},
        {"name": "Nou Barris", "price_m2": 16.5, "vulnerability": 9, "lat": 41.4400, "lon": 2.1800}
    ]
    
    data = []
    for d in districts:
        count = 30
        m2 = np.random.normal(70, 10, count) # Realistic apartment sizes
        
        # 1. GREEN MOBILITY ACCESS (Bicing Density)
        # Hypothesis: Higher in tourist/wealthy areas, lower in vulnerable peripheries
        green_access = (10 - d['vulnerability']) * 1.5 + np.random.normal(0, 0.5, count)
        
        # 2. AIR QUALITY INDEX (NO2 Levels)
        # Hypothesis: More traffic in the center (Ciutat Vella/Eixample)
        air_pollution = (10 - d['vulnerability']) * 4 + np.random.normal(0, 2, count)
        
        # 3. HOUSING AFFORDABILITY (Rent Price)
        # Influenced by Area, Air Quality (negatively) and Green Access (Gentrifiers)
        base_rent = m2 * d['price_m2']
        gentrification_premium = green_access * 75 # Proximity to green transport raises rent
        vulnerability_discount = d['vulnerability'] * -80 # Lower rent in vulnerable areas
        
        rent_prices = base_rent + gentrification_premium + vulnerability_discount + np.random.normal(0, 15, count)
        
        for i in range(count):
            data.append([
                d['name'], d['lat'], d['lon'], 
                round(m2[i], 2), 
                d['vulnerability'], 
                round(green_access[i], 2), 
                round(air_pollution[i], 2),
                round(rent_prices[i], 2)
            ])
            
    df = pd.DataFrame(data, columns=[
        'district', 'lat', 'lon', 'sq_meters', 
        'social_vulnerability', 'green_mobility_access', 'air_pollution_index', 'rent_price'
    ])
    
    df.to_csv('data/bcn_housing_mobility.csv', index=False)
    print("\n" + "="*60)
    print("✅ SOCIAL IMPACT DATA GENERATED: bcn_housing_mobility.csv")
    print("🌍 FOCUS: Urban Equity, Air Quality, and Green Gentrification.")
    print("="*60 + "\n")

if __name__ == "__main__":
    generate_social_impact_data()