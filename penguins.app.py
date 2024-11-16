cintel-04-local
from shiny.express import input, ui, render
from shinywidgets import render_plotly
import plotly.express as px
from palmerpenguins import load_penguins
from shiny import reactive
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO


# Load the Palmer Penguins dataset
penguins = load_penguins()

# Set the page options with the title "Penguin Data Exploration"
ui.page_opts(title="Penguin Data Exploration - Katie McGaughey", fillable=True)

# Add a Shiny UI sidebar for user interaction
with ui.sidebar(position="right", bg="#f8f8f8", open="open"):  # Set sidebar open by default
    ui.h2("Sidebar")  # Sidebar header

    # Dropdown input for choosing a column
    ui.input_selectize(
        "selected_attribute",
        "Select column to visualize",
        choices=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
        selected="bill_length_mm",
    )

    # Numeric input for Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Plotly bin Count", 12, min=1, max=30)

    # Slider input for Seaborn bins
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 5, 50, 15, step=5)

    # Checkbox group to filter species
    ui.input_checkbox_group(
        "selected_species_list",
        "Select Species",
        choices=["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie"],
        inline=True,
    )

 # Horizontal rule in the sidebar
    ui.hr()

    # Link to GitHub repository
    ui.h5("GitHub Code Repository")
    ui.a(
        "View on GitHub",
        href="https://github.com/k363m611/cintel-02-data",
        target="_blank",
    )

# Main content layout
with ui.layout_columns():
    # Plotly Histogram
    with ui.card():
        ui.card_header("Plotly Histogram")

        @render_plotly
        def plotly_histogram():
            return px.histogram(
                penguins,
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
                color_discrete_sequence=["red", "blue", "green"]
            )


    # Data Table
    with ui.card():
        ui.card_header("Data Table")

        @render.data_frame
        def data_table():
            return penguins

# Data Grid
    with ui.card():
        ui.card_header("Data Grid")

        @render.data_frame
        def data_grid():
            return penguins

# Display the Scatterplot and Seaborn Histogram
with ui.layout_columns():
    # Plotly Scatterplot
    with ui.card():
        ui.card_header("Plotly Scatterplot: Body Mass vs. Bill Depth")

        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                data_frame=penguins,
                x="body_mass_g",
                y="bill_depth_mm",
                color="species",
                labels={"bill_depth_mm": "Bill Depth (mm)", "body_mass_g": "Body Mass (g)"},
                color_discrete_sequence=["red", "blue", "green"]
            )

 # Seaborn Histogram
    with ui.card():
        ui.card_header("Seaborn Histogram: Body Mass")

        @render.plot
        def seaborn_histogram():
            fig, ax = plt.subplots()
            sns.histplot(
                data=penguins, x="body_mass_g", hue="species", bins=input.seaborn_bin_count(), ax=ax,palette=["red", "black", "green"]
            )
            ax.set_xlabel("Mass (g)")
            ax.set_ylabel("Count")
            ax.set_title("Body Mass Distribution (Seaborn)")
            return fig

  # Summary Statistics Table
    with ui.card():
        ui.card_header("Summary Statistics")

        @render.data_frame
        def summary_table():
            summary = penguins.describe()
            return summary.reset_index()  # Reset index for display

# Density plot
with ui.card():
    ui.card_header("Seaborn Density Plot: Body Mass by Species")

    @render.plot
    def seaborn_density_plot():
        fig, ax = plt.subplots()
        sns.kdeplot(
            data=penguins,
            x="body_mass_g",
            hue="species",
            ax=ax,
            fill=True,
            palette=["red", "black", "green"]
        )
        ax.set_xlabel("Body Mass (g)")
        ax.set_ylabel("Density")
        ax.set_title("Body Mass Density by Species")
        return fig
