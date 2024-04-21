import matplotlib.pyplot as plt

# Data
class_scores = {'profitability': 8.0, 'leverage_coverage': 3.1, 'efficiency': 2.0}
class_weights = {'profitability': 0.3, 'leverage_coverage': 0.55, 'efficiency': 0.15}
score = 4.405
rating = 'A'

# Create a figure and axis
fig, ax = plt.subplots(figsize=(15, 3))

# Horizontal bar chart
classes = list(class_scores.keys())
weighted_scores = [class_scores[cls] * class_weights[cls] for cls in classes]

bar_height = 0.5
ax.barh(0, score, height=bar_height, color='lightgray', edgecolor='black')
ax.set_xlim(0, score)

left = 0
for i, (cls, weighted_score) in enumerate(zip(classes, weighted_scores)):
    ax.barh(0, weighted_score, height=bar_height, left=left, color=plt.cm.viridis(i/len(classes)))
    ax.text(left + weighted_score/2, 0, f'{cls}: {class_scores[cls]:.1f}\n{class_weights[cls]:.2%}', ha='center', va='center', fontsize=12, color='white')
    left += weighted_score

# Customize the chart
ax.set_yticks([])
ax.set_xlabel('Credit Rating Score')
ax.set_title(f'Credit Rating Score Composition: {score:.3f} (Rating: {rating})')

# Add a secondary x-axis on top for the 0 to 100% scale
ax2 = ax.twiny()

ax2.set_xticks(range(0, 101, 10))
#ax2.set_xticklabels([f'{x}%' for x in range(0, int(score) + 1, int(score) // 10)])

plt.tight_layout()
#plt.show()


