# Solar Panel Sizing Tool ☀️

The Solar Panel Sizing Tool is designed to help you analyze the ideal size of solar panels, tailored for the Berlin subsidy program for mini balcony solar powerplants. This program restricts the inverter power to 600 watts. 🏙️

This tool calculates various metrics, including energy generation and payback time, based on user-defined parameters and solar radiation data. It provides insights to optimize your solar power setup. 📊

In general, it's worth considering a somewhat oversized panel (e.g. 800-1400 Watts of nominal power) even if the inverter is limited to 600 watts (for the Berlin program). This ensures that you can still produce 600 watts even in 
suboptimal conditions. ♻️

## Table of Contents
- [Installation](#installation-)
- [Usage](#usage-)
- [Output](#output-)
- [License](#license-)

## Installation 🚀

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/riparise/solar-panel-sizing-tool.git
   ```

2. Change to the project directory:

   ```bash
   cd solar-panel-sizing-tool
   ```

3. Install the required Python packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

## Usage 🧰

To use the Solar Panel Sizing Tool, follow these steps:

1. Modify the YAML configuration file (`config.yml`) with your specific parameters. Here's the parameters list:

   - `latitude` and `longitude`: The geographical coordinates of your location in degrees. Default: latitude=52.52 and longitude=13.40
   - `panel_azimuth`: The azimuth angle of your solar panels in degrees (0=north, 90=east, 180=south, 270=west). Default: 245
   - `panel_angle`: The tilt angle of your solar panels in degrees (0=horizontal, 90=vertical). Default: 90
   - `max_inverter_power`: The maximum inverter power in Watts. Default: 600
   - `inverter_efficiency`: The average inverter efficiency. Default: 0.91
   - `energy_cost_per_kwh`: Energy rates in EUR/kWh. Default: 0.35
   - `installation_costs` and `subsidy_amount`: Additional installation costs and subsidies in EUR. Default: subsidy=500 and installation_costs=30
   - `system_losses`: Other losses that are not associated with inverter efficiency like panels degradation, glass transmittance, dirt, and more. Default: 0.05
   - `horizon_data`: List of elevation of horizon in degrees, at arbitrary number of equally spaced azimuths clockwise from north. (e.g., for a south-faced façade with buildings nearby [90, 90, 90, 20, 20, 20, 90, 90])
   - `pv_tech`: Cell technologies. Options are 'crystSi', 'CIS', 'CdTe', or 'Unknown'. Default: 'crystSi'
   - `panel_sizes`: List of the panel sizes to be analyzed in Watts. Default: [600, 800, 1000, 1100, 1200, 1300, 1400]
   - `panel_price`: Costs of the panels. Either as a single coefficient (in EUR per Watt of nominal power), or as a list with the cost of each panel size analyzed. Default: 0.52
   - `unused_energy`: Percentage of the energy generated that is not directly used. Assuming there is no buyback. Defaults: 0.4

   Feel free to modify these parameters to match your specific setup and requirements.

2. Run the main script using Python:

   ```bash
   python main.py
   ```

   The script will load the configuration from the `config.yml` file, retrieve solar radiation data, calculate trade-off metrics, and plot the results.

3. Review the generated plots and metrics to make an informed decision about the ideal size of solar panels for your mini balcony solar powerplant.

## Output 📈

The tool generates three plots to help you analyze your solar panel sizing:

![Output Example](/output_example.png)

1. **Average Hourly Energy Generation per kW of installed solar panels:** This plot shows the average historical solar generation (per kW of installed solar panel) throughout the day, categorized by seasons (Winter, Spring, Summer, Fall). Use this graph mostly for a sanity check if the 
   input is correct (e.g. if there is shadow in the early morning, you should see it in the graph).
ch
2. **Energy Generation and payoff time vs. panel size** This plot illustrates the relationship between panel size and energy generation per year, along with the payback time.

3. **Return over time vs. panel size:** This plot displays the balance evolution in euros for different panel sizes, allowing you to compare the financial aspects of your solar powerplant.

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Radiation data from 2006 and 2020 is taken from [European Photovoltaic Geographical Information System](https://re.jrc.ec.europa.eu/api/v5_2/) using the amazing [pvlib](https://pvlib-python.readthedocs.io/en/stable/) library for the 
complicated PV calculations.

This is my first public repo, so feel to leave any comments, suggestions or open merge request.

