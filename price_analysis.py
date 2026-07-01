import sys
import io
import logging
import pandas as pd
import matplotlib.pyplot as plt

if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(message)s')

def load_data():
    logging.info("Loading data...")
    df = pd.read_csv('cleaned_restaurants.csv', encoding='utf-8-sig')
    logging.info("Loaded: " + str(len(df)) + " restaurants")
    return df

def analyze_price_range(df):
    logging.info("Analyzing price range distribution...")
    price_range_counts = df['Price range'].value_counts().sort_index()
    total = len(df)
    price_range_percentages = (price_range_counts / total) * 100
    return price_range_counts, price_range_percentages, total

def print_price_range_results(price_range_counts, price_range_percentages, total):
    print("\n" + "="*80)
    print(" PROBLEM STATEMENT: PRICE RANGE DISTRIBUTION")
    print("\n" + "="*80)

    print("\n Price Range Distribution:")
    print("-" * 70)
    print("Price Category | Count | Percentage  | Visual")
    print("-" * 70)

    for price_range, count in price_range_counts.items():
        pct = price_range_percentages[price_range]
        bar = "█" * int (pct/2)
        label = PRICE_LABELS.get(price_range, str(price_range))
        print(" {:<14} | {:5d} | {:7.2f}%    | {}".format(label, count, pct, bar))
    print("\n" + "-"*70)
    print("ANSWER:")
    print("-"*70)

    #Finding the most common
    most_common_range = price_range_counts.idxmax()
    most_common_count = price_range_counts.max()
    most_common_pct = price_range_percentages.max()

    #Finding the least common
    least_common_range = price_range_counts.idxmin()
    least_common_count = price_range_counts.min()
    least_common_pct = price_range_percentages.min()

    print("\n Most common Price range: " + str(most_common_range))
    print("   Restaurants: " + str(most_common_count))
    print("   Percentage: " + str(most_common_pct))

    print("\n Least common Price range: " + str(least_common_range))
    print("   Restaurants: " + str(least_common_count))
    print("   Percentage: " + str(least_common_pct))

    print("Total Restaurants: " + str(total))
    print("-" * 70)
    sys.stdout.flush()

#Exporting Results
PRICE_LABELS = { 1: "Low Cost", 2: "Moderate", 3: "Expensive", 4: "Luxury"}

def export_price_range_results(price_range_counts, price_range_percentages):
    logging.info("Exporting Results...")
    export_df = pd.DataFrame({
        'Price Range': [PRICE_LABELS[p] for p in price_range_counts.index],
        'Count' : price_range_counts.values,
        'Percentage' : price_range_percentages.values.round(2)
    })

    export_df.to_csv('price_range_distribution.csv', index=False, encoding='utf-8-sig')
    logging.info("Exported: price_range_distribution.csv")

#Creating Visualization
COLORS = ['#4E79A7', '#F28E2B', '#59A14F', '#E15759']
def create_price_range_visualization(price_range_counts, price_range_percentages, total):
    logging.info("Creating visualization...")

    fig, axes = plt.subplots(1, 2, figsize=(14,5))

    #Bar Chart- Count Distribution 
    ax1 = axes[0]
    bars1 = ax1.bar(price_range_counts.index, price_range_counts.values, color=COLORS[:len(price_range_counts)], edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Number of Restaurants', fontweight='bold')
    ax1.set_xlabel('Price Category', fontweight='bold')
    ax1.set_title("Price Range Distribution\n({} Restaurants)".format(total), fontweight='bold', fontsize=14)
    ax1.set_xticks(price_range_counts.index)
    ax1.set_xticklabels([PRICE_LABELS[p] for p in price_range_counts.index], rotation=15)
    ax1.grid(axis='y', alpha=0.3)

    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.,height, '{:.0f}'.format(height), ha='center', va='bottom', fontweight='bold')

    #Pie Chart - Percentage
    ax2 = axes[1]
    price_labels = [PRICE_LABELS[p] for p  in price_range_counts.index]
    ax2.pie(price_range_counts.values, labels=price_labels, autopct='%1.2f%%', 
            colors=COLORS[:len(price_range_counts)], startangle=90,textprops={'fontweight' :'bold'}, wedgeprops={'edgecolor': 'black', 'linewidth':2}, labeldistance=1.05, pctdistance=0.75)
    ax2.set_title('Pie Chart - Price Distribution Percentage', fontweight='bold', fontsize=14)
    ax2.axis('equal')

    plt.tight_layout()
    plt.savefig('price_range_distribution.png', dpi=300, bbox_inches='tight')
    logging.info("Charts saved: price_range_distribution.png")
    plt.show()

#Printing Summary
def print_summary(price_range_counts, price_range_percentages, total):
    print("\n" + "="*80)
    print(" SUMMARY - PRICE DISTRIBUTION ANALYSIS")
    print("="*80)

    print("\n Total Restaurants Analyzed: " + str(total))

    print("\nPrice Range Breakdown:")
    for price_range, count in price_range_counts.items():
        label = PRICE_LABELS.get(price_range, str(price_range))
        pct = price_range_percentages[price_range]
        print(" {}: {} restaurants ({:.2f}%)".format(label, count, pct))

    print("\nFiles Created:")
    print("  1. price_range_distribution.csv")
    print("  2. price_range_distribution.png")

    print("\n" + "="*80 + "\n")

#Main Function

def main():
    print("\n" + "="*80)
    print("PRICE RANGE DISTRIBUTION ANALYSIS")
    print("="*80 + "\n")

    try:
        df = load_data() #Loading the data
        price_range_counts, price_range_percentages, total = analyze_price_range(df) #Analyzing the price range
        print_price_range_results(price_range_counts, price_range_percentages, total) #Display results
        export_price_range_results(price_range_counts, price_range_percentages) #Create Visualization
        create_price_range_visualization(price_range_counts, price_range_percentages, total)
        print_summary(price_range_counts, price_range_percentages, total)
        logging.info("Analysis Complete!")
        print("Analysis Completed Successfully!")

    except Exception as e:
        logging.error("Error: " + str(e))
        import traceback
        traceback.print_exc()
        
if __name__ == "__main__":
    main()
     