import pandas as pd

def update_hotspots():
    print("🔄 Processing raw data...")
    df = pd.read_csv('sightings.csv') 
    print(f"   - Found {len(df)} raw sightings.")

    # 2. THE GRID ALGORITHM
    # Rounding coordinates effectively snaps them to a grid.
    # 3 decimal places ≈ 110m resolution (perfect for Home Ranges)
    df['lat_grid'] = df['latitude'].round(3)
    df['lon_grid'] = df['longitude'].round(3)

    # 3. AGGREGATE (Count sightings per grid)
    # We group by common name + grid coordinates
    hotspots = df.groupby(
        ['common_name', 'lat_grid', 'lon_grid']
    ).size().reset_index(name='sighting_count')

    # 4. FILTER (The "Verified" Logic)
    # Only keep areas where the bird was seen at least 3 times
    verified_hotspots = hotspots[hotspots['sighting_count'] >= 3].copy()

    print(f"   - Compressed into {len(verified_hotspots)} verified Hotspots.")

    # 5. FORMATTING
    # Rename grid columns back to lat/lon so the App understands them
    verified_hotspots.rename(columns={'lat_grid': 'lat', 'lon_grid': 'lon'}, inplace=True)

    # 6. MERGE & SAVE
    # Combine the untouchable DEMO target with our new Verified Hotspots
    final_df = pd.concat([verified_hotspots], ignore_index=True)

    output_file = 'final_hotspots.csv'
    final_df.to_csv(output_file, index=False)  
    print("✅ Hotspots updated!")

if __name__ == "__main__":
    update_hotspots()