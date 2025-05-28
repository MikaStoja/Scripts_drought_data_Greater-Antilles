import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text

# Load the data
file_path = 'CUBA.xlsx' #change the name of island 
spi12_df = pd.read_excel(file_path, sheet_name='SPI12')

# Convert 'Date' column to datetime
spi12_df['Date'] = pd.to_datetime(spi12_df['Date'], errors='coerce')

# Identify drought episodes separated by empty rows (NaN in 'Date')
episodes = []
start_idx = 0
episode_indices = spi12_df[spi12_df['Date'].isnull()].index

for end_idx in episode_indices:
    episode = spi12_df.iloc[start_idx:end_idx]
    episode = episode.dropna(subset=['Duration', 'Severity'], how='all')
    if not episode.empty:
        duration = episode['Duration'].max()
        severity = episode['Severity'].min()  # Most negative = most severe
        episodes.append({'data': episode, 'duration': duration, 'severity': severity})
    start_idx = end_idx + 1

# Add final episode if the file doesn't end with an empty row
final_episode = spi12_df.iloc[start_idx:]
final_episode = final_episode.dropna(subset=['Duration', 'Severity'], how='all')
if not final_episode.empty:
    duration = final_episode['Duration'].max()
    severity = final_episode['Severity'].min()
    episodes.append({'data': final_episode, 'duration': duration, 'severity': severity})

# Print total number of detected episodes
print(f"\nNumber of detected drought episodes: {len(episodes)}")

# Create the plot
plt.figure(figsize=(10, 6))

# Plot all episodes in gray
for ep in episodes:
    plt.plot(ep['data']['Duration'], ep['data']['Severity'], color='gray', alpha=0.5)

# Sort episodes by most negative severity only
sorted_episodes = sorted(episodes, key=lambda x: x['severity'])

# Highlight the 5 most severe episodes with different colors
highlight_colors = ['red', 'blue', 'green', 'orange', 'purple']
texts = []

for i, ep in enumerate(sorted_episodes[:5]):
    plt.plot(ep['data']['Duration'], ep['data']['Severity'], color=highlight_colors[i], linewidth=2)
    start_date = ep['data']['Date'].iloc[0]
    end_date = ep['data']['Date'].iloc[-1]
    label = f"{start_date.strftime('%Y-%m')} - {end_date.strftime('%Y-%m')}"
    text = plt.text(ep['data']['Duration'].iloc[-1], ep['data']['Severity'].iloc[-1],
                    label, fontsize=14, color=highlight_colors[i])
    texts.append(text)

# Adjust labels to prevent overlap
adjust_text(texts)

# Axes and title configuration
plt.xlim(1, 24)
# plt.ylim(-8, 0)

# Plot formatting
plt.xlabel('Duration from onset (months)', fontsize=18)
plt.ylabel('Drought Severity', fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

# Save the figure
plt.savefig('SPI12_drought_episodes_Cuba.png', dpi=300, bbox_inches='tight')
plt.show()
