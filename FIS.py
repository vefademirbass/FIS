import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
import datetime



damage = ctrl.Antecedent(np.arange(0, 11, 1), 'damage')
accessibility = ctrl.Antecedent(np.arange(0, 11, 1), 'accessibility')
population = ctrl.Antecedent(np.arange(0, 11, 1), 'population')
priority = ctrl.Consequent(np.arange(0, 101, 1), 'priority')


damage['low'] = fuzz.trimf(damage.universe, [0, 0, 5])
damage['medium'] = fuzz.trimf(damage.universe, [2, 5, 8])
damage['high'] = fuzz.trimf(damage.universe, [5, 10, 10])


accessibility['poor'] = fuzz.trimf(accessibility.universe, [0, 0, 5])
accessibility['moderate'] = fuzz.trimf(accessibility.universe, [2, 5, 8])
accessibility['good'] = fuzz.trimf(accessibility.universe, [5, 10, 10])

population['low'] = fuzz.trimf(population.universe, [0, 0, 5])
population['medium'] = fuzz.trimf(population.universe, [2, 5, 8])
population['high'] = fuzz.trimf(population.universe, [5, 10, 10])


priority['low'] = fuzz.trimf(priority.universe, [0, 0, 30])
priority['medium'] = fuzz.trimf(priority.universe, [20, 40, 60])
priority['medium_high'] = fuzz.trimf(priority.universe, [40, 60, 80])
priority['high'] = fuzz.trimf(priority.universe, [60, 80, 90])
priority['very_high'] = fuzz.trimf(priority.universe, [80, 100, 100])



rules = []


def decide_priority(d_level, a_level, p_level):
    
    score = 0
    
    
    if d_level == 'high': score += 3
    elif d_level == 'medium': score += 2
    else: score += 1
    
    
    if p_level == 'high': score += 3
    elif p_level == 'medium': score += 2
    else: score += 1
    
    
    if a_level == 'good': score += 3
    elif a_level == 'moderate': score += 2
    else: score += 1 

    
    if score >= 8: return 'very_high'
    elif score >= 7: return 'high'
    elif score >= 6: return 'medium_high'
    elif score >= 5: return 'medium'
    else: return 'low'


levels_damage = ['low', 'medium', 'high']
levels_access = ['poor', 'moderate', 'good']
levels_pop = ['low', 'medium', 'high']

rule_count = 1
print(f"{'Rule ID':<10} {'Damage':<10} {'Access':<10} {'Pop':<10} {'-> Output'}")
print("-" * 60)

for d in levels_damage:
    for a in levels_access:
        for p in levels_pop:
           
            output_label = decide_priority(d, a, p)
            
            
            rule = ctrl.Rule(damage[d] & accessibility[a] & population[p], priority[output_label])
            rules.append(rule)
            
            print(f"R{rule_count:<9} {d:<10} {a:<10} {p:<10} -> {output_label}")
            rule_count += 1


priority_ctrl = ctrl.ControlSystem(rules)
priority_sim = ctrl.ControlSystemSimulation(priority_ctrl)




np.random.seed(42)


NUM_SAMPLES = 100
data_list = []

print(f"\n{NUM_SAMPLES} samples being generated")

for i in range(NUM_SAMPLES):
    
    
    val_damage = round(np.random.uniform(0, 10), 1)
    val_access = round(np.random.uniform(0, 10), 1)
    val_pop    = round(np.random.uniform(0, 10), 1)

    
    priority_sim.input['damage'] = val_damage
    priority_sim.input['accessibility'] = val_access
    priority_sim.input['population'] = val_pop

    try:
        priority_sim.compute()
        score = priority_sim.output['priority']
    except:
        score = 0 

    
    priority_cat = ""
    if score >= 80: priority_cat = "Very High"
    elif score >= 60: priority_cat = "High"
    elif score >= 45: priority_cat = "Med-High"
    elif score >= 30: priority_cat = "Medium"
    else: priority_cat = "Low"



    data_list.append({
        "Scenario_ID": i + 1,
        "Damage_Severity": val_damage,
        "Accessibility": val_access,
        "Population_Exposure": val_pop,
        "Priority_Score": round(score, 2),
        "Priority_Level": priority_cat
    })




df_results = pd.DataFrame(data_list)


print("\n--- First 10 Sample From Generated Data Set ---")

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
print(df_results.head(10))


print("\n--- Statistical Summary---")
print(df_results.describe())


zaman_damgasi = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


excel_filename = f"simulation_results_{zaman_damgasi}.xlsx"

writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')

df_results.to_excel(writer, index=False, sheet_name='Simulation_Data')


workbook  = writer.book
worksheet = writer.sheets['Simulation_Data']


header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#D7E4BC', 'border': 1})


worksheet.set_column('A:A', 12) # Scenario ID
worksheet.set_column('B:D', 18) # Inputlar
worksheet.set_column('E:E', 15) # Score
worksheet.set_column('F:G', 20) # Priority & Team


writer.close()

print(f"\nExcel File Created: '{excel_filename}'")