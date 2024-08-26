"""

file: analysis.py    
Author: Mohamed Badr    
    
description: Trying to merge index data with IO data in the form of extensions
    
"""
#%%

from pathlib import Path
import pymrio
import numpy as np
import pandas as pd
import country_converter as coco
import matplotlib.pyplot as plt
import seaborn as sns

#%%
#Get EXIOBASE
downloads_path = str(Path.home() / "Downloads")
exio_path = downloads_path + '/IOT_2022_pxp.zip'
exio3 = pymrio.parse_exiobase3(path=exio_path)
exio3.calc_all()  # Calculate all necessary data

#%%
#Get the sum of inputs

Z = exio3.Z
Z_sum = Z.sum()
Z_sum
#%%
F = exio3.impacts.F.iloc[0:5]
VA = exio3.impacts.F.iloc[0:1]

#%%
#Get total Inputs (this is the base of the new extension)
total_inputs = Z_sum + VA 
total_inputs
# %%

#import Corruption perception index scores

CPI = pd.read_excel('data/CPI2023_Global_Results__Trends.xlsx')
CPI = CPI.iloc[3:].reset_index(drop=True)
CPI = CPI.iloc[:, :4]
CPI.columns = ['state','ISO3','region','CPI_2023']
CPI['ISO2'] = coco.convert(names=CPI['ISO3'], to='ISO2') #Get two letter country code
CPI
# %%
#Get rest of the world values 

Europe_RW = ['ISL', 'MLT', 'ROU','HUN', 'GEO', 'ARM', 'MNE','MDA','MKD','KSV'
         ,'ALB', 'BLR','SRB','UKR','BIH','AZE']
Middle_east_RW = ['ARE','ISR','QAT','SAU','JOR','KWT','OMN','BHR','TUN','MAR',
                  'DZA','EGY','IRN','LBN','IRQ','LBY','YEM','SYR']
Latin_America_RW = ['URY','BRB','CHL', 'BHS', 'VCT', 'DMA', 'CRI', 'LCA', 'GRD', 'JAM', 'CUB', 'TTO', 
    'COL', 'GUY', 'SUR', 'ARG', 'DOM','PAN','ECU','SLV','BOL', 'PRY', 'GTM', 'HND', 'HTI', 'NIC', 'VEN']
Asia_RW = ['NZL','SGP','HKG','BTN','FJI','MYS','VNM','VUT','SLB','TLS','MDV','NPL','THA','PHL',
           'LKA','MNG','PAK','PNG','LAO','BGD','KHM','AFG','MMR','PRK']
Africa_RW = ['SYC', 'CPV', 'BWA', 'RWA', 'MUS', 'NAM', 'STP', 'BEN', 'GHA', 'SEN', 
             'BFA','CIV', 'TZA', 'LSO', 'ETH', 'GMB', 'ZMB', 'SLE', 'MWI', 'AGO', 'NER',
            'KEN', 'TGO', 'DJI', 'SWZ', 'MRT', 'GAB', 'MLI', 'CMR', 'GIN', 'UGA',
            'LBR', 'MDG', 'MOZ', 'NGA', 'CAF', 'ZWE', 'COG', 'GNB', 'ERI', 'BDI',
            'TCD', 'COM', 'COD', 'SDN', 'GNQ', 'SSD', 'SOM']


#%%
#append EU rest of the world
Europe_RW_df = CPI[CPI['ISO3'].isin(Europe_RW)]
average_EU = Europe_RW_df['CPI_2023'].mean()
average_EU
average_EU_row = {'state': 'Rest of the World: Europe', 'ISO3': 'NA','region':'WE/EU','CPI_2023':average_EU,'ISO2':'WE'}
CPI.loc[len(CPI)] = average_EU_row

#%%
#append Africa rest of the world
AF_RW_df = CPI[CPI['ISO3'].isin(Africa_RW)]
average_AF = AF_RW_df['CPI_2023'].mean()
average_AF
average_AF_row = {'state': 'Rest of the World: Africa', 'ISO3': 'NA','region':'Africa','CPI_2023':average_AF,'ISO2':'WF'}
CPI.loc[len(CPI)] = average_AF_row

#%%
#append Latin America rest of the world
LA_RW_df = CPI[CPI['ISO3'].isin(Latin_America_RW)]
average_LA = LA_RW_df['CPI_2023'].mean()
average_LA
average_LA_row = {'state': 'Rest of the World: Latin America', 'ISO3': 'NA','region':'Latin America','CPI_2023':average_LA,'ISO2':'WL'}
CPI.loc[len(CPI)] = average_LA_row

#%%
#append Asia rest of the world
asia_RW_df = CPI[CPI['ISO3'].isin(Asia_RW)]
average_asia = asia_RW_df['CPI_2023'].mean()
average_asia
average_asia_row = {'state': 'Rest of the World: Asia', 'ISO3': 'NA','region':'Asia','CPI_2023':average_asia,'ISO2':'WA'}
CPI.loc[len(CPI)] = average_asia_row

#%%
#append Middle East rest of the world
ME_RW_df = CPI[CPI['ISO3'].isin(Middle_east_RW)]
average_ME = ME_RW_df['CPI_2023'].mean()
average_ME
average_ME_row = {'state': 'Rest of the World: Middle East', 'ISO3': 'NA','region':'Middle East','CPI_2023':average_ME,'ISO2':'WM'}
CPI.loc[len(CPI)] = average_ME_row


# %%
CPI
# %%
total_inputs_df = pd.DataFrame(data= total_inputs.unstack())
total_inputs_df = total_inputs_df.reset_index()
total_inputs_df =total_inputs_df.merge(CPI, right_on= 'ISO2', left_on='region',how= 'left')
total_inputs_df
# %%

extension = total_inputs_df[['region_x','sector',0,'CPI_2023']]
extension.columns = ['region','sector','total_inputs','CPI_2023']
extension

#%%

#Create a sector specific factor

highly_vulnerable = [ 'Aluminium and aluminium products','Aluminium ores and concentrates','Charcoal',
 'Chemical and fertilizer minerals, salt and other mining and quarrying products n.e.c.',
 'Chemicals nec',
 'Coal Tar',
 'Coke Oven Coke',
 'Coke oven gas',
 'Coking Coal','Crude petroleum and services related to crude oil extraction, excluding surveying','Distribution and trade services of electricity',
 'Distribution services of gaseous fuels through mains', 'Gas Coke',
 'Gas Works Gas',
 'Gas/Diesel Oil',
 'Gasoline Type Jet Fuel','Heavy Fuel Oil','Inert/metal/hazardous waste for treatment: landfill','Iron ores',
 'Kerosene',
 'Kerosene Type Jet Fuel',
 'Lead, zinc and tin and products thereof',
 'Lead, zinc and tin ores and concentrates', 'Motor Gasoline',
 'Motor vehicles, trailers and semi-trailers (34)',
 'N-fertiliser','Natural Gas Liquids',
 'Natural gas and services related to natural gas extraction, excluding surveying','Nuclear fuel',
 'Oil/hazardous waste for treatment: incineration', 'Oxygen Steel Furnace Gas',
 'P- and other fertiliser','Patent Fuel',
 'Peat',
 'Petroleum Coke', 'Services auxiliary to financial intermediation (67)','Sub-Bituminous Coal',
 'Uranium and thorium ores (12)']

medium_vulnerable = [ 
                     'Air transport services (62)','Animal products nec','Anthracite',
                     'Ash for treatment, Re-processing of ash into clinker','Aviation Gasoline','BKB/Peat Briquettes',
                    'Basic iron and steel and of ferro-alloys and first products thereof',
                    'Beverages',
                    'Biodiesels',
                    'Biogas',
                    'Biogasoline', 'Sewage sludge for treatment: biogasification and land application',
 'Steam and hot water supply services',
 'Stone',
                    'Bitumen',
                    'Blast Furnace Gas',
                    'Bottles for treatment, Recycling of bottles by direct reuse',
                    'Bricks, tiles and construction products, in baked clay',  'Cement, lime and plaster',
 'Ceramic goods',
 'Cereal grains nec', 'Electrical machinery and apparatus n.e.c. (31)',
 'Electricity by Geothermal',
 'Electricity by biomass and waste',
 'Electricity by coal',
 'Electricity by gas',
 'Electricity by hydro',
 'Electricity by nuclear',
 'Electricity by petroleum and other oil derivatives',
 'Electricity by solar photovoltaic',
 'Electricity by solar thermal',
 'Electricity by tide, wave, ocean',
 'Electricity by wind',
 'Electricity nec', 'Glass and glass products',
 'Health and social work services (85)', 'Leather and leather products (19)',
 'Lignite/Brown Coal',
 'Liquefied Petroleum Gases (LPG)',
 'Lubricants', 'Machinery and equipment n.e.c. (29)',
 'Manure (biogas treatment)',
 'Manure (conventional treatment)',
 'Meat animals nec',
 'Meat products nec','Naphtha', 'Nickel ores and concentrates',
 'Non-specified Petroleum Products', 'Other Bituminous Coal',
 'Other Hydrocarbons',
 'Other Liquid Biofuels',
 'Other business services (74)',
 'Other land transportation services',
 'Other non-ferrous metal ores and concentrates',
 'Other non-ferrous metal products',
 'Other non-metallic mineral products',
 'Other services (93)',
 'Other transport equipment (35)',
 'Other waste for treatment: waste water treatment', 'Plastic waste for treatment: incineration',
 'Plastic waste for treatment: landfill',
 'Plastics, basic',
 'Post and telecommunication services (64)', 'Precious metal ores and concentrates',
 'Precious metals',
 'Printed matter and recorded media (22)',  'Private households with employed persons (95)',
 'Processed rice',  'Products of forestry, logging and related services (02)',
 'Products of meat cattle',
 'Products of meat pigs',
 'Products of meat poultry',  'Public administration and defence services; compulsory social security services (75)',
 'Pulp',
 'Radio, television and communication equipment and apparatus (32)',
 'Railway transportation services','Refinery Feedstocks',
 'Refinery Gas',
 'Renting services of machinery and equipment without operator and of personal and household goods (71)', 'Research and development services (73)',
 'Retail  trade services, except of motor vehicles and motorcycles; repair services of personal and household goods (52)',
 'Retail trade services of motor fuel',
 'Rubber and plastic products (25)',  'Secondary aluminium for treatment, Re-processing of secondary aluminium into new aluminium',
 'Secondary construction material for treatment, Re-processing of secondary construction material into aggregates',
 'Secondary copper for treatment, Re-processing of secondary copper into new copper',
 'Secondary glass for treatment, Re-processing of secondary glass into new glass',
 'Secondary lead for treatment, Re-processing of secondary lead into new lead',
 'Secondary other non-ferrous metals for treatment, Re-processing of secondary other non-ferrous metals into new other non-ferrous metals',
 'Secondary paper for treatment, Re-processing of secondary paper into new pulp',
 'Secondary plastic for treatment, Re-processing of secondary plastic into new plastic',
 'Secondary preciuos metals for treatment, Re-processing of secondary preciuos metals into new preciuos metals',
 'Secondary raw materials',
 'Secondary steel for treatment, Re-processing of secondary steel into new steel','Textiles (17)',
 'Textiles waste for treatment: incineration',
 'Textiles waste for treatment: landfill',
 'Tobacco products (16)',
 'Transmission services of electricity',
 'Transportation services via pipelines', 'Wholesale trade and commission trade services, except of motor vehicles and motorcycles (51)',
 'Wood and products of wood and cork (except furniture); articles of straw and plaiting materials (20)',
 'Wood material for treatment, Re-processing of secondary wood material into new wood material',
 'Wood waste for treatment: incineration',
 'Wood waste for treatment: landfill',
 'Wool, silk-worm cocoons',
 'products of Vegetable oils and fats'

                     ]

low_vulnerable = ['Additives/Blending Components', 'Cattle', 'Collected and purified water, distribution services of water (41)',
 'Computer and related services (72)',
 'Construction work (45)',
 'Copper ores and concentrates',
 'Copper products',
 'Crops nec','Dairy products','Education services (80)', 'Ethane',
 'Extra-territorial organizations and bodies',
 'Fabricated metal products, except machinery and equipment (28)',
 'Financial intermediation services, except insurance and pension funding services (65)',
 'Fish and other fishing products; services incidental of fishing (05)',
 'Fish products',
 'Food products nec',
 'Food waste for treatment: biogasification and land application',
 'Food waste for treatment: composting and land application',
 'Food waste for treatment: incineration',
 'Food waste for treatment: landfill',
 'Food waste for treatment: waste water treatment',
 'Foundry work services', 'Furniture; other manufactured goods n.e.c. (36)','Hotel and restaurant services (55)','Inland water transportation services',
 'Insurance and pension funding services, except compulsory social security services (66)',
 'Intert/metal waste for treatment: incineration', 'Medical, precision and optical instruments, watches and clocks (33)',
 'Membership organisation services n.e.c. (91)','Office machinery and computers (30)',
 'Oil seeds','Paddy rice',
 'Paper and paper products',
 'Paper and wood waste for treatment: composting and land application',
 'Paper for treatment: landfill',
 'Paper waste for treatment: biogasification and land application',
 'Paper waste for treatment: incineration',
 'Paraffin Waxes','Pigs','Plant-based fibers', 'Poultry','Raw milk',
 'Real estate services (70)',
 'Recreational, cultural and sporting services (92)', 'Sale, maintenance, repair of motor vehicles, motor vehicles parts, motorcycles, motor cycles parts and accessoiries',
 'Sand and clay',
 'Sea and coastal water transportation services','Vegetables, fruit, nuts','Sugar', 
 'Sugar cane, sugar beet','Supporting and auxiliary transport services; travel agency services (63)','Wearing apparel; furs (18)',
 'Wheat',
 'White Spirit & SBP']

# %%
#assign
extension.loc[extension['sector'].isin(low_vulnerable), 'sector_vulnerability'] = 'Low'
extension.loc[extension['sector'].isin(medium_vulnerable), 'sector_vulnerability'] = 'Medium'
extension.loc[extension['sector'].isin(highly_vulnerable), 'sector_vulnerability'] = 'High'


extension.loc[extension['sector'].isin(low_vulnerable), 'sector_factor'] = 0.9
extension.loc[extension['sector'].isin(medium_vulnerable), 'sector_factor'] = 1
extension.loc[extension['sector'].isin(highly_vulnerable), 'sector_factor'] = 1.1

#%%
#get regional factor
extension['regional_corruption'] = 100 - extension['CPI_2023']

#get sector adjusted regional corruption score
extension['sector_adjusted_regional_corruption'] = extension['regional_corruption'] * extension['sector_factor']

#Get extension value
extension['extension_value'] = (extension['sector_adjusted_regional_corruption']/100) * extension['total_inputs']
extension

# %%
#create Extension
corruption_extension = extension[['region','sector','extension_value']]
corruption_extension = corruption_extension.set_index(['region', 'sector'])
corruption_extension.T
# %%

def calc_corr():
    """
    Gets corruption footprint for all regions 
    
    """
    regions = set(exio3.L.columns.get_level_values(level =0))
    empty =[]
    
    for region in regions:
        Y = exio3.Y[region].sum(axis=1)
        D = corruption_extension.T@exio3.L@Y
        empty.append([region,float(D)])
    
    results = pd.DataFrame(empty)
    return results
    
results = calc_corr()        
#%%
#plot total corruption footprints
results.columns = ['region','Corruption Footprint']
results

plt.figure(figsize=(18, 6))
sns.barplot(x='region', y='Corruption Footprint', data=results, color='black')

# Add titles and labels
plt.title('Corruption Footprint by Region')
plt.xlabel('Region')
plt.ylabel('Corruption Footprint')

# Add grid
plt.grid(True, which='both', linestyle='--', linewidth=0.7)

# Display the plot
plt.show()
# %%
#Merge with Value Added
Value_added = exio3.impacts.D_cba.iloc[0].groupby('region').sum()
Value_added 
# %%

total_input_grouped = total_inputs.T.groupby('region').sum()
total_input_grouped
#%%
totalinputs_corruption = results.merge(total_input_grouped, left_on= 'region', right_index=True, how = 'left' )
totalinputs_corruption.columns = ['region','Corruption Footprint','Total Inputs']
totalinputs_corruption
# %%
#compare total inputs to the extensions
corruption_extension_grouped = corruption_extension.groupby('region').sum()
corruption_extension_grouped_merged = corruption_extension_grouped.merge(total_input_grouped,
                                                                         left_index=True,
                                                                         right_index=True, 
                                                                         how = 'left')
corruption_extension_grouped_merged.columns = ['Corruption Extension','Total Inputs']
corruption_extension_grouped_merged
#%%

plt.figure(figsize=(20, 6))

# Number of regions
n_regions = len(corruption_extension_grouped_merged.index)

# Bar width
bar_width = 0.35

# Bar positions
r1 = np.arange(n_regions)
r2 = r1 + bar_width

# Plotting Corruption Footprint bars
plt.bar(r1, corruption_extension_grouped_merged['Corruption Extension'], color='black', width=bar_width, label='Corruption Extension')

# Plotting Value Added bars
plt.bar(r2, corruption_extension_grouped_merged['Total Inputs'], color='red', width=bar_width, label='Total Inputs')

# Adding labels and titles
plt.xlabel('Region', fontweight='bold')
plt.ylabel('Values', fontweight='bold')
plt.title('Corruption Footprint and Total Inputs by Region')

# Setting the x-ticks and labels
plt.xticks(r1 + bar_width / 2, corruption_extension_grouped_merged.index)

# Adding grid for better readability
plt.grid(True, which='both', linestyle='--', linewidth=0.7)

# Adding the legend
plt.legend()

# Display the plot
plt.show()


#%%


corruption_extension_grouped_merged['ratio'] = corruption_extension_grouped_merged['Corruption Extension']/corruption_extension_grouped_merged['Total Inputs']
corruption_extension_grouped_merged.sort_values('ratio', ascending=True)

# %%
