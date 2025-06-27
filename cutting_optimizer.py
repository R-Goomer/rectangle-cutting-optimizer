import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def calculate_placement(paper_width_mm, paper_height_mm, rect_width_mm, rect_height_mm):
    """Calculate placement for both orientations"""
    
    # Orientation 1: rectangle as-is
    cols_1 = int(paper_width_mm // rect_width_mm)
    rows_1 = int(paper_height_mm // rect_height_mm)
    total_1 = cols_1 * rows_1
    
    # Orientation 2: rectangle rotated 90°
    cols_2 = int(paper_width_mm // rect_height_mm)
    rows_2 = int(paper_height_mm // rect_width_mm)
    total_2 = cols_2 * rows_2
    
    return {
        'orientation_1': {
            'cols': cols_1, 'rows': rows_1, 'total': total_1, 
            'rect_w': rect_width_mm, 'rect_h': rect_height_mm,
            'name': f'{rect_width_mm}×{rect_height_mm}mm rectangles'
        },
        'orientation_2': {
            'cols': cols_2, 'rows': rows_2, 'total': total_2, 
            'rect_w': rect_height_mm, 'rect_h': rect_width_mm,
            'name': f'{rect_height_mm}×{rect_width_mm}mm rectangles (rotated)'
        }
    }

def create_cutting_diagrams(paper_width_mm, paper_height_mm, placements):
    """Create cutting diagrams for both orientations"""
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))
    
    # Scale for better visualization
    scale = min(10/paper_width_mm, 6/paper_height_mm) * 1000
    
    paper_w_scaled = paper_width_mm * scale
    paper_h_scaled = paper_height_mm * scale
    
    for ax, (key, placement) in zip([ax1, ax2], placements.items()):
        # Draw paper background (white sheet)
        paper_rect = patches.Rectangle((0, 0), paper_w_scaled, paper_h_scaled, 
                                     linewidth=3, edgecolor='black', facecolor='white')
        ax.add_patch(paper_rect)
        
        # Draw rectangles with black borders
        rect_w_scaled = placement['rect_w'] * scale
        rect_h_scaled = placement['rect_h'] * scale
        
        for row in range(placement['rows']):
            for col in range(placement['cols']):
                x = col * rect_w_scaled
                y = row * rect_h_scaled
                
                # Black border rectangles on white background
                rect = patches.Rectangle((x, y), rect_w_scaled, rect_h_scaled,
                                       linewidth=2, edgecolor='black', facecolor='none')
                ax.add_patch(rect)
        
        # Calculate waste
        used_width = placement['cols'] * placement['rect_w']
        used_height = placement['rows'] * placement['rect_h']
        total_area = paper_width_mm * paper_height_mm
        used_area = used_width * used_height
        waste_area = total_area - used_area
        waste_percentage = (waste_area / total_area) * 100
        
        # Add wastage lines from center edge to last rectangle
        # Right edge wastage (horizontal)
        right_waste = paper_width_mm - used_width
        if right_waste > 0:
            # Line from center of right edge to last rectangle
            start_x = paper_w_scaled
            start_y = paper_h_scaled / 2
            end_x = used_width * scale
            end_y = paper_h_scaled / 2
            
            ax.plot([start_x, end_x], [start_y, end_y], 'r-', linewidth=2, alpha=0.8)
            ax.plot([start_x, end_x], [start_y, end_y], 'ro', markersize=4)
            
            # Add text showing wastage length
            mid_x = (start_x + end_x) / 2
            ax.text(mid_x, start_y + 0.05, f'{right_waste:.1f}mm', 
                   ha='center', va='bottom', fontsize=10, color='red', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        # Top edge wastage (vertical)
        top_waste = paper_height_mm - used_height
        if top_waste > 0:
            # Line from center of top edge to last rectangle
            start_x = paper_w_scaled / 2
            start_y = paper_h_scaled
            end_x = paper_w_scaled / 2
            end_y = used_height * scale
            
            ax.plot([start_x, end_x], [start_y, end_y], 'r-', linewidth=2, alpha=0.8)
            ax.plot([start_x, end_x], [start_y, end_y], 'ro', markersize=4)
            
            # Add text showing wastage length
            mid_y = (start_y + end_y) / 2
            ax.text(start_x + 0.05, mid_y, f'{top_waste:.1f}mm', 
                   ha='left', va='center', fontsize=10, color='red', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        # Set axis properties
        ax.set_xlim(-0.1, paper_w_scaled + 0.1)
        ax.set_ylim(-0.1, paper_h_scaled + 0.1)
        ax.set_aspect('equal')
        ax.set_title(f'{placement["name"]}\n'
                    f'Grid: {placement["cols"]} × {placement["rows"]} = {placement["total"]} rectangles\n'
                    f'Waste: {waste_area:.0f}mm² ({waste_percentage:.1f}%)', 
                    fontsize=12, fontweight='bold', pad=20)
        
        # Add dimensions as text
        ax.text(paper_w_scaled/2, -0.05, f'Paper: {paper_width_mm}×{paper_height_mm}mm', 
                ha='center', va='top', fontsize=10, transform=ax.transData)
        
        # Remove ticks
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add grid lines for better visualization
        ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    return fig

def main():
    st.set_page_config(page_title="Rectangle Cutting Optimizer", layout="wide")
    
    st.title("Rectangle Cutting Optimizer")
    st.write("Compare both orientations to find the best cutting layout")
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Paper Dimensions (mm)")
        paper_width = st.number_input("Paper Width (mm)", min_value=1.0, value=1828.8, step=0.1)
        paper_height = st.number_input("Paper Height (mm)", min_value=1.0, value=889.0, step=0.1)
    
    with col2:
        st.subheader("Rectangle Dimensions (mm)")
        rect_width = st.number_input("Rectangle Width (mm)", min_value=1.0, value=360.0, step=0.1)
        rect_height = st.number_input("Rectangle Height (mm)", min_value=1.0, value=325.0, step=0.1)
    
    # Calculate placements
    placements = calculate_placement(paper_width, paper_height, rect_width, rect_height)
    
    # Display results summary
    st.subheader("Results Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Orientation 1", 
                 f"{placements['orientation_1']['total']} rectangles",
                 f"{placements['orientation_1']['cols']}×{placements['orientation_1']['rows']} grid")
    
    with col2:
        st.metric("Orientation 2", 
                 f"{placements['orientation_2']['total']} rectangles",
                 f"{placements['orientation_2']['cols']}×{placements['orientation_2']['rows']} grid")
    
    with col3:
        best_orientation = 1 if placements['orientation_1']['total'] >= placements['orientation_2']['total'] else 2
        best_total = max(placements['orientation_1']['total'], placements['orientation_2']['total'])
        st.metric("Best Option", f"Orientation {best_orientation}", f"{best_total} rectangles")
    
    # Create and display diagrams
    st.subheader("Cutting Layouts")
    fig = create_cutting_diagrams(paper_width, paper_height, placements)
    st.pyplot(fig)
    
    # Additional information
    st.subheader("Detailed Information")
    
    for i, (key, placement) in enumerate(placements.items(), 1):
        with st.expander(f"Orientation {i}: {placement['name']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Grid Layout:** {placement['cols']} columns × {placement['rows']} rows")
                st.write(f"**Total Rectangles:** {placement['total']}")
                st.write(f"**Rectangle Size:** {placement['rect_w']}×{placement['rect_h']}mm")
            
            with col2:
                used_width = placement['cols'] * placement['rect_w']
                used_height = placement['rows'] * placement['rect_h']
                total_area = paper_width * paper_height
                used_area = used_width * used_height
                waste_area = total_area - used_area
                waste_percentage = (waste_area / total_area) * 100
                
                st.write(f"**Used Area:** {used_area:.0f}mm²")
                st.write(f"**Waste Area:** {waste_area:.0f}mm²")
                st.write(f"**Efficiency:** {100-waste_percentage:.1f}%")

if __name__ == "__main__":
    main()